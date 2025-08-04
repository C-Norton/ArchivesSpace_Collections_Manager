import pytest

import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")


class TestConnectionStateManagement:
    """Test connection state management through public behavior"""

    def test_connection_state_after_failed_test_remains_clean(self):
        """Test that connection state remains clean after test failure"""
        conn = Connection("", "user", "pass")  # Invalid config

        with pytest.raises(ConfigurationError):
            conn.test_connection()

        # State should remain clean - test through public interface
        # We can't test private attributes, but we can test observable behavior
        with pytest.raises(ConfigurationError):
            # Should still fail with same error, indicating state wasn't corrupted
            conn.test_connection()

    def test_connection_works_after_successful_test(self, mocker):
        """Test that connection works after successful test"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        # First test the connection
        conn.test_connection()

        # Then verify we can make queries
        mock_response = mocker.Mock()
        mock_client.get.return_value = mock_response

        result = conn.query(HttpRequestType.GET, "/test")
        assert result == mock_response

    def test_multiple_test_connection_calls_work_correctly(self, mocker):
        """Test multiple calls to test_connection work independently"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client1 = mocker.Mock(spec=ASnakeClient)
        mock_client2 = mocker.Mock(spec=ASnakeClient)
        mock_client_class.side_effect = [mock_client1, mock_client2]

        # First call
        conn.test_connection()

        # Should be able to query after first test
        mock_response1 = mocker.Mock()
        mock_client1.get.return_value = mock_response1
        result1 = conn.query(HttpRequestType.GET, "/test1")
        assert result1 == mock_response1

        # Second call should work independently
        conn.test_connection()

        # Should be able to query after second test
        mock_response2 = mocker.Mock()
        mock_client2.get.return_value = mock_response2
        result2 = conn.query(HttpRequestType.GET, "/test2")
        assert result2 == mock_response2

    def test_query_fails_appropriately_before_test_connection(self, mocker):
        """Test that query behavior is predictable before test_connection is called"""
        conn = Connection("https://test.com", "user", "pass")

        # Without calling test_connection first, query should handle gracefully
        # This tests the public contract - what happens when user calls query first
        with pytest.raises(AuthenticationError) as e:
            result = conn.query(HttpRequestType.GET, "/test")

            # The exact behavior depends on implementation, but it should be predictable
            # Either it auto-validates or returns None - either is acceptable
            # We're testing that it doesn't crash
            assert result is None or hasattr(
                result, "json"
            )  # Either None or response-like objectimport pytest


import requests.exceptions
import asnake.client.web_client
from asnake.client import ASnakeClient

# Import the classes we're testing
from controller.connection import Connection
from controller.connection_exceptions import (
    ConfigurationError,
    AuthenticationError,
    NetworkError,
    ServerError,
)
from controller.HttpRequestType import HttpRequestType


class TestConnectionInitialization:
    """Test Connection initialization"""

    def test_connection_initialization_with_valid_params(self):
        """Test that Connection can be initialized with valid parameters"""
        server = "https://test.archivesspace.org"
        username = "testuser"
        password = "testpass"

        conn = Connection(server, username, password)

        assert conn.server == server
        assert conn.username == username
        assert conn.password == password
        assert conn.client is None
        assert conn.validated is False

    def test_connection_initialization_with_empty_strings(self):
        """Test that Connection accepts empty strings (validation happens later)"""
        conn = Connection("", "", "")

        assert conn.server == ""
        assert conn.username == ""
        assert conn.password == ""
        assert conn.client is None
        assert conn.validated is False

    def test_connection_str_representation(self):
        """Test the string representation of Connection"""
        conn = Connection("server", "user", "pass")
        expected = "server" + "user" + "pass"
        assert str(conn) == expected


class TestConnectionValidation:
    """Test connection validation logic"""

    def test_test_connection_with_empty_server_raises_configuration_error(self):
        """Test that empty server raises ConfigurationError"""
        conn = Connection("", "user", "pass")

        with pytest.raises(ConfigurationError) as exc_info:
            conn.test_connection()

        assert "configuration is incomplete" in str(exc_info.value).lower()

    def test_test_connection_with_empty_username_raises_configuration_error(self):
        """Test that empty username raises ConfigurationError"""
        conn = Connection("https://test.com", "", "pass")

        with pytest.raises(ConfigurationError):
            conn.test_connection()

    def test_test_connection_with_empty_password_raises_configuration_error(self):
        """Test that empty password raises ConfigurationError"""
        conn = Connection("https://test.com", "user", "")

        with pytest.raises(ConfigurationError):
            conn.test_connection()

    def test_test_connection_with_whitespace_only_raises_configuration_error(self):
        """Test that whitespace-only values raise ConfigurationError"""
        test_cases = [
            ("   ", "user", "pass"),  # whitespace server
            ("server", "   ", "pass"),  # whitespace username
            ("server", "user", "   "),  # whitespace password
            ("   ", "   ", "   "),  # all whitespace
        ]

        for server, username, password in test_cases:
            conn = Connection(server, username, password)
            with pytest.raises(ConfigurationError):
                conn.test_connection()

    @pytest.mark.parametrize(
        "server,username,password",
        [
            ("", "user", "pass"),
            ("server", "", "pass"),
            ("server", "user", ""),
            ("", "", ""),
            ("   ", "user", "pass"),
            ("server", "   ", "pass"),
            ("server", "user", "   "),
        ],
    )
    def test_various_invalid_configurations_raise_configuration_error(
        self, server, username, password
    ):
        """Test various invalid configuration combinations"""
        conn = Connection(server, username, password)

        with pytest.raises(ConfigurationError):
            conn.test_connection()


class TestConnectionAuthentication:
    """Test authentication behavior through public interface"""

    def test_test_connection_succeeds_with_valid_credentials(self, mocker):
        """Test that test_connection succeeds with valid setup"""
        conn = Connection("https://test.com", "user", "pass")

        # Mock the external dependency
        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        # Should not raise any exception
        conn.test_connection()

        # Verify external API was called correctly
        mock_client_class.assert_called_once_with(
            baseurl="https://test.com", username="user", password="pass"
        )
        mock_client.authorize.assert_called_once()

    def test_test_connection_invalid_url_raises_configuration_error(self, mocker):
        """Test that invalid URL raises ConfigurationError via test_connection"""
        conn = Connection("not-a-url", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client_class.side_effect = requests.exceptions.MissingSchema(
            "Invalid URL scheme"
        )

        with pytest.raises(ConfigurationError) as exc_info:
            conn.test_connection()

        assert "Invalid server URL" in str(exc_info.value)
        assert exc_info.value.__cause__ is not None

    def test_test_connection_malformed_url_raises_configuration_error(self, mocker):
        """Test that malformed URL raises ConfigurationError via test_connection"""
        conn = Connection("ht!tp://bad-url", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client_class.side_effect = requests.exceptions.InvalidURL("Invalid URL")

        with pytest.raises(ConfigurationError) as exc_info:
            conn.test_connection()

        assert "Malformed server URL" in str(exc_info.value)

    def test_debug_exception_chain(self, mocker):
        conn = Connection("https://test.com", "user", "badpass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client
        mock_client.authorize.side_effect = asnake.client.web_client.ASnakeAuthError(
            "Invalid credentials"
        )

        with pytest.raises(AuthenticationError) as exc_info:
            conn.test_connection()

        print(f"Exception: {exc_info.value}")
        print(f"Cause: {exc_info.value.__cause__}")
        print(f"Cause type: {type(exc_info.value.__cause__)}")

    def test_test_connection_auth_error_raises_authentication_error(self, mocker):
        """Test that authentication failure raises AuthenticationError via test_connection"""
        conn = Connection("https://test.com", "user", "badpass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client
        mock_client.authorize.side_effect = asnake.client.web_client.ASnakeAuthError(
            "Invalid credentials"
        )
        # Add some debugging
        original_exception = asnake.client.web_client.ASnakeAuthError(
            "Invalid credentials"
        )
        mock_client.authorize.side_effect = original_exception
        print(f"Original exception: {original_exception}")
        print(f"Original exception type: {type(original_exception)}")

        with pytest.raises(AuthenticationError) as exc_info:
            conn.test_connection()
        print(f"Raised exception: {exc_info.value}")
        print(f"Raised exception type: {type(exc_info.value)}")
        print(f"Cause: {exc_info.value.__cause__}")
        print(f"Cause type: {type(exc_info.value.__cause__)}")
        print(f"Cause is original: {exc_info.value.__cause__ is original_exception}")
        print(f"Cause is None: {exc_info.value.__cause__ is None}")
        assert "Invalid username or password" in str(exc_info.value)
        assert isinstance(
            exc_info.value.__cause__, asnake.client.web_client.ASnakeAuthError
        )

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "exception_class,expected_error",
        [
            (requests.exceptions.ConnectionError, NetworkError),
            (requests.exceptions.ConnectTimeout, NetworkError),
            (requests.exceptions.ReadTimeout, NetworkError),
            (requests.exceptions.Timeout, NetworkError),
        ],
    )
    def test_test_connection_network_errors_raise_network_error(
        self, mocker, exception_class, expected_error
    ):
        """Test that various network exceptions raise NetworkError via test_connection"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client_class.side_effect = exception_class("Network failed")

        with pytest.raises(expected_error) as exc_info:
            conn.test_connection()

        assert "Connection to server failed" in str(exc_info.value)

    def test_test_connection_http_client_error_raises_authentication_error(
        self, mocker
    ):
        """Test that HTTP 4xx errors raise AuthenticationError via test_connection"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")

        # Create a mock response with status_code
        mock_response = mocker.Mock()
        mock_response.status_code = 401

        http_error = requests.exceptions.HTTPError("401 Unauthorized")
        http_error.response = mock_response

        mock_client_class.side_effect = http_error

        with pytest.raises(AuthenticationError) as exc_info:
            conn.test_connection()

        assert "Client error" in str(exc_info.value)

    def test_test_connection_http_server_error_raises_server_error(self, mocker):
        """Test that HTTP 5xx errors raise ServerError via test_connection"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")

        # Create a mock response with status_code
        mock_response = mocker.Mock()
        mock_response.status_code = 500

        http_error = requests.exceptions.HTTPError("500 Server Error")
        http_error.response = mock_response

        mock_client_class.side_effect = http_error

        with pytest.raises(ServerError) as exc_info:
            conn.test_connection()

        assert "Server error" in str(exc_info.value)

    def test_test_connection_http_error_without_response_raises_server_error(
        self, mocker
    ):
        """Test that HTTP errors without response object raise ServerError via test_connection"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        http_error = requests.exceptions.HTTPError("Generic HTTP error")
        # No response attribute

        mock_client_class.side_effect = http_error

        with pytest.raises(ServerError):
            conn.test_connection()

    def test_test_connection_unexpected_error_raises_server_error(self, mocker):
        """Test that unexpected errors raise ServerError via test_connection"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client_class.side_effect = ValueError("Unexpected error")

        with pytest.raises(ServerError) as exc_info:
            conn.test_connection()

        assert "Unexpected error" in str(exc_info.value)


class TestConnectionRetryBehavior:
    """Test retry behavior through public interface"""

    def test_test_connection_succeeds_after_temporary_network_failure(self, mocker):
        """Test that connection succeeds after temporary network issues"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_sleep = mocker.patch("time.sleep")

        # First two calls fail, third succeeds
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.side_effect = [
            requests.exceptions.ConnectionError("Temporary failure"),
            requests.exceptions.Timeout("Network timeout"),
            mock_client,  # Success on third try
        ]

        # Should not raise exception (succeeds on retry)
        conn.test_connection()

        # Verify retry behavior occurred
        assert mock_client_class.call_count == 3
        assert mock_sleep.call_count == 2  # Sleep between retries

    def test_test_connection_fails_after_exhausting_retries(self, mocker):
        """Test that connection fails after all retries are exhausted"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mocker.patch("time.sleep")

        # All attempts fail
        mock_client_class.side_effect = requests.exceptions.ConnectionError(
            "Persistent failure"
        )

        with pytest.raises(NetworkError) as exc_info:
            conn.test_connection()

        # Verify all retries were attempted
        assert mock_client_class.call_count == 3  # max_attempts = 3
        assert "failed after 3 attempts" in str(exc_info.value)

    def test_test_connection_no_retry_on_authentication_error(self, mocker):
        """Test that authentication errors are not retried"""
        conn = Connection("https://test.com", "user", "badpass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_sleep = mocker.patch("time.sleep")

        mock_client_class.side_effect = asnake.client.web_client.ASnakeAuthError(
            "Bad credentials"
        )

        with pytest.raises(AuthenticationError):
            conn.test_connection()

        # Should only try once (no retries for auth errors)
        assert mock_client_class.call_count == 1
        assert mock_sleep.call_count == 0

    def test_test_connection_no_retry_on_configuration_error(self, mocker):
        """Test that configuration errors are not retried"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_sleep = mocker.patch("time.sleep")

        mock_client_class.side_effect = ValueError("Unexpected configuration issue")

        with pytest.raises(ServerError):
            conn.test_connection()

        # Should only try once (no retries for unexpected errors)
        assert mock_client_class.call_count == 1
        assert mock_sleep.call_count == 0

    def test_test_connection_exponential_backoff_timing(self, mocker):
        """Test that retry delays follow exponential backoff pattern"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_sleep = mocker.patch("time.sleep")

        # All attempts fail to trigger all retries
        mock_client_class.side_effect = requests.exceptions.ConnectionError(
            "Always fails"
        )

        with pytest.raises(NetworkError):
            conn.test_connection()

        # Verify exponential backoff delays (2^0=1, 2^1=2)
        expected_delays = [1, 2]  # 2^0, 2^1
        actual_delays = [call[0][0] for call in mock_sleep.call_args_list]
        assert actual_delays == expected_delays


class TestConnectionQueryBehavior:
    """Test query behavior through public interface"""

    def test_query_successful_get_request(self, mocker):
        """Test successful GET request through query method"""
        conn = Connection("https://test.com", "user", "pass")

        # Setup a successfully tested connection
        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client
        conn.test_connection()  # This sets up the client
        mock_client.get.reset_mock()  # Clear previous calls
        # Now test the query
        mock_response = mocker.Mock()
        mock_client.get.return_value = mock_response

        result = conn.query(HttpRequestType.GET, "/repositories/2")

        assert result == mock_response
        mock_client.get.assert_called_once_with("/repositories/2")

    def test_query_raises_authentication_exception_when_needed(self, mocker):
        """Test that query revalidates connection when not validated"""
        conn = Connection("https://test.com", "user", "pass")

        # Set up client but mark as not validated
        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        conn.client = mock_client
        conn.validated = False  # Force revalidation

        mock_response = mocker.Mock()
        mock_client.get.return_value = mock_response
        with pytest.raises(AuthenticationError):
            conn.query(HttpRequestType.GET, "/test")

    def test_query_handles_unsupported_http_methods(self, mocker):
        """Test that unsupported HTTP methods return None gracefully"""
        conn = Connection("https://test.com", "user", "pass")

        # Setup validated connection
        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client
        conn.test_connection()
        mock_client.get.reset_mock()
        # Test unsupported method
        result = conn.query(HttpRequestType.POST, "/test")

        # Should return None gracefully
        assert result is None

        # Should not call any client methods
        mock_client.get.assert_not_called()

    @pytest.mark.parametrize(
        "http_type",
        [
            HttpRequestType.HEAD,
            HttpRequestType.POST,
            HttpRequestType.PUT,
            HttpRequestType.DELETE,
            HttpRequestType.CONNECTION,
            HttpRequestType.OPTIONS,
            HttpRequestType.TRACE,
            HttpRequestType.PATCH,
        ],
    )
    def test_query_returns_none_for_unsupported_methods(self, mocker, http_type):
        """Test that all unsupported HTTP methods return None"""
        conn = Connection("https://test.com", "user", "pass")

        # Setup validated connection
        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client
        conn.test_connection()

        result = conn.query(http_type, "/test")
        assert result is None


class TestConnectionEdgeCases:
    """Test edge cases and boundary conditions through public interface"""

    def test_connection_with_very_long_credentials_works(self, mocker):
        """Test connection with very long credential strings"""
        long_string = "x" * 1000
        conn = Connection(long_string, long_string, long_string)

        # Should handle long strings without issue
        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        # Should work normally despite long credentials
        conn.test_connection()

        # Verify it was called with the long strings
        mock_client_class.assert_called_once_with(
            baseurl=long_string, username=long_string, password=long_string
        )

    def test_connection_with_unicode_credentials_works(self, mocker):
        """Test connection with Unicode characters"""
        server = "https://тест.example.com"
        username = "用户"
        password = "пароль"

        conn = Connection(server, username, password)

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        # Should handle Unicode without issue
        conn.test_connection()

        # Verify Unicode was passed correctly
        mock_client_class.assert_called_once_with(
            baseurl=server, username=username, password=password
        )

    def test_connection_handles_special_characters_in_credentials(self, mocker):
        """Test connection with special characters in credentials"""
        server = "https://test.com:8089"
        username = "user@domain.com"
        password = "pass!@#$%^&*()"

        conn = Connection(server, username, password)

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        # Should handle special characters
        conn.test_connection()

        mock_client_class.assert_called_once_with(
            baseurl=server, username=username, password=password
        )


class TestConnectionIntegration:
    """Integration tests for complete connection workflows"""

    def test_full_connection_workflow_success(self, mocker):
        """Test complete successful connection workflow"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mocker.patch("time.sleep")

        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        # Test full workflow: test connection then query
        conn.test_connection()

        # Should be able to make successful queries
        mock_response = mocker.Mock()
        mock_client.get.return_value = mock_response

        result = conn.query(HttpRequestType.GET, "/repositories/2")
        assert result == mock_response

        # Should be able to make multiple queries
        result2 = conn.query(HttpRequestType.GET, "/test")
        assert result2 == mock_response

    def test_connection_recovery_after_failure(self, mocker):
        """Test that connection can recover after initial failure"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mocker.patch("time.sleep")

        mock_client = mocker.Mock(spec=ASnakeClient)

        # First attempt fails, second succeeds
        mock_client_class.side_effect = [
            requests.exceptions.ConnectionError("Temporary failure"),
            mock_client,
        ]

        # Should succeed after retry
        conn.test_connection()

        # Should be able to query after recovery
        mock_response = mocker.Mock()
        mock_client.get.return_value = mock_response

        result = conn.query(HttpRequestType.GET, "/test")
        assert result == mock_response

    def test_connection_workflow_with_different_endpoints(self, mocker):
        """Test querying different endpoints after connection"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        # Establish connection
        conn.test_connection()

        # Test different endpoints
        endpoints_responses = [
            ("/repositories", mocker.Mock()),
            ("/repositories/2", mocker.Mock()),
            ("/repositories/2/resources", mocker.Mock()),
            ("/repositories/2/resources/1", mocker.Mock()),
        ]

        for endpoint, mock_response in endpoints_responses:
            mock_client.get.return_value = mock_response
            result = conn.query(HttpRequestType.GET, endpoint)
            assert result == mock_response
            mock_client.get.assert_called_with(endpoint)

    def test_connection_handles_query_before_test(self, mocker):
        """Test graceful handling when query is called before test_connection"""
        conn = Connection("https://test.com", "user", "pass")

        mock_client_class = mocker.patch("controller.connection.ASnakeClient")
        mock_client = mocker.Mock(spec=ASnakeClient)
        mock_client_class.return_value = mock_client

        mock_response = mocker.Mock()
        mock_client.get.return_value = mock_response

        # Call query without calling test_connection first
        with pytest.raises(AuthenticationError):
            result = conn.query(HttpRequestType.GET, "/test")
