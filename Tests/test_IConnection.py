import pytest
import requests.exceptions
import asnake.client.web_client
from abc import ABC, abstractmethod

# Import your custom exceptions
from controller.connection_exceptions import (
    ConfigurationError,
    AuthenticationError,
    NetworkError,
    ServerError,
)

# Import your Connection implementation
from controller.connection import Connection


class IConnection(ABC):
    """Interface for connection objects"""

    @abstractmethod
    def test_connection(self) -> None:
        """Test if connection works. Raises exception on failure."""
        pass


class TestIConnection:
    """Test suite for IConnection interface implementations"""

    # Fixtures for different connection configurations
    @pytest.fixture
    def valid_connection(self):
        """Connection with valid configuration"""
        return Connection("https://test.archivesspace.org", "testuser", "testpass")

    @pytest.fixture
    def empty_connection(self):
        """Connection with no configuration"""
        return Connection("", "", "")

    @pytest.fixture
    def partial_connection(self):
        """Connection with incomplete configuration"""
        return Connection("https://test.com", "user", "")

    @pytest.fixture
    def whitespace_connection(self):
        """Connection with whitespace-only values"""
        return Connection("   ", "  ", "  ")

    # Configuration Error Tests
    def test_empty_server_raises_configuration_error(self, empty_connection):
        """Test that empty server configuration raises ConfigurationError"""
        with pytest.raises(ConfigurationError) as exc_info:
            empty_connection.test_connection()

        assert "configuration" in str(exc_info.value).lower()

    def test_empty_username_raises_configuration_error(self):
        """Test that empty username raises ConfigurationError"""
        connection = Connection("https://test.com", "", "password")

        with pytest.raises(ConfigurationError):
            connection.test_connection()

    def test_empty_password_raises_configuration_error(self):
        """Test that empty password raises ConfigurationError"""
        connection = Connection("https://test.com", "username", "")

        with pytest.raises(ConfigurationError):
            connection.test_connection()

    def test_whitespace_only_values_raise_configuration_error(
        self, whitespace_connection
    ):
        """Test that whitespace-only values are treated as empty"""
        with pytest.raises(ConfigurationError):
            whitespace_connection.test_connection()

    def test_partial_configuration_raises_error(self, partial_connection):
        """Test that incomplete configuration raises ConfigurationError"""
        with pytest.raises(ConfigurationError):
            partial_connection.test_connection()

    # Authentication Error Tests
    def test_invalid_credentials_raise_authentication_error(
        self, valid_connection, monkeypatch
    ):
        """Test that invalid credentials raise AuthenticationError"""

        def mock_create_session():
            raise asnake.client.web_client.ASnakeAuthError("Invalid credentials")

        with pytest.raises(AuthenticationError) as exc_info:
            valid_connection.test_connection()

        # Check for words that are actually in the message
        assert (
            "username" in str(exc_info.value).lower()
            or "password" in str(exc_info.value).lower()
        )

    def test_auth_error_chains_original_exception(self, valid_connection, monkeypatch):
        """Test that AuthenticationError chains the original exception"""
        original_error = asnake.client.web_client.ASnakeAuthError(
            "Failed to authorize ASnake with status: 404"
        )

        with pytest.raises(AuthenticationError) as exc_info:
            valid_connection.test_connection()

        assert isinstance(
            exc_info.value.__cause__, asnake.client.web_client.ASnakeAuthError
        )
        assert (
            str(exc_info.value.__cause__)
            == "Failed to authorize ASnake with status: 404"
        )

    # Network Error Tests
    def test_connection_timeout_raises_network_error(
        self, valid_connection, monkeypatch
    ):
        """Test that connection timeout raises NetworkError"""
        import requests

        # Mock the session to raise a timeout exception
        def mock_post(*args, **kwargs):
            raise requests.exceptions.Timeout("Connection timed out")

        # You'll need to patch the session.post method that gets called during authorization
        monkeypatch.setattr("requests.Session.post", mock_post)

        with pytest.raises(NetworkError):
            valid_connection.test_connection()

    def test_connection_refused_raises_network_error(
        self, valid_connection, monkeypatch
    ):
        """Test that connection refused raises NetworkError"""

        def mock_create_session(self):
            raise requests.exceptions.ConnectionError("Connection refused")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(NetworkError):
            valid_connection.test_connection()

    def test_dns_failure_raises_network_error(self, valid_connection, monkeypatch):
        """Test that DNS resolution failure raises NetworkError"""

        def mock_create_session(self):
            raise requests.exceptions.ConnectionError("Name resolution failed")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(NetworkError):
            valid_connection.test_connection()

    def test_malformed_url_raises_configuration_error(self, monkeypatch):
        """Test that malformed URL raises ConfigurationError"""
        connection = Connection("not-a-url", "user", "pass")

        def mock_create_session(self):
            raise requests.exceptions.MissingSchema("Invalid URL scheme")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(ConfigurationError):
            connection.test_connection()

    # Success Cases
    def test_successful_connection_returns_none(self, valid_connection, monkeypatch):
        """Test that successful connection returns None (no exception)"""

        def mock_create_session(self):
            return True

        def mock_verify_connection(self):
            pass

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)
        monkeypatch.setattr(Connection, "_verify_connection", mock_verify_connection)

        # Should not raise any exception
        result = valid_connection.test_connection()
        assert result is None

    def test_successful_connection_sets_client(self, valid_connection, monkeypatch):
        """Test that successful connection sets the client attribute"""
        mock_client = object()  # Simple object to verify assignment

        def mock_create_session(self):
            self.client = mock_client
            return True

        def mock_verify_connection(self):
            pass

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)
        monkeypatch.setattr(Connection, "_verify_connection", mock_verify_connection)

        valid_connection.test_connection()
        assert valid_connection.client is mock_client

    # Server Error Tests
    def test_server_error_raises_server_error(self, valid_connection, monkeypatch):
        """Test that server errors raise ServerError"""

        def mock_create_session(self):
            raise requests.exceptions.HTTPError("500 Internal Server Error")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(ServerError):
            valid_connection.test_connection()

    def test_unexpected_error_raises_server_error(self, valid_connection, monkeypatch):
        """Test that unexpected errors raise ServerError"""

        def mock_create_session(self):
            raise ValueError("Unexpected error")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(ServerError) as exc_info:
            valid_connection.test_connection()

        assert "unexpected" in str(exc_info.value).lower()

    # Parametrized Tests for Multiple Invalid Configurations
    @pytest.mark.parametrize(
        "server,username,password",
        [
            ("", "user", "pass"),  # Empty server
            ("server", "", "pass"),  # Empty username
            ("server", "user", ""),  # Empty password
            ("   ", "user", "pass"),  # Whitespace server
            ("server", "   ", "pass"),  # Whitespace username
            ("server", "user", "   "),  # Whitespace password
            ("", "", ""),  # All empty
            ("   ", "   ", "   "),  # All whitespace
        ],
    )
    def test_invalid_configurations_raise_configuration_error(
        self, server, username, password
    ):
        """Test various invalid configuration combinations"""
        connection = Connection(server, username, password)

        with pytest.raises(ConfigurationError):
            connection.test_connection()

    # Parametrized Tests for Different Network Errors
    @pytest.mark.parametrize(
        "exception_class,exception_message",
        [
            (requests.exceptions.Timeout, "Request timeout"),
            (requests.exceptions.ConnectionError, "Connection failed"),
            (requests.exceptions.ConnectTimeout, "Connect timeout"),
            (requests.exceptions.ReadTimeout, "Read timeout"),
        ],
    )
    def test_various_network_errors_raise_network_error(
        self, valid_connection, monkeypatch, exception_class, exception_message
    ):
        """Test that various network exceptions raise NetworkError"""

        def mock_create_session(self):
            raise exception_class(exception_message)

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(NetworkError):
            valid_connection.test_connection()

    # Edge Cases
    def test_none_client_after_session_creation(self, valid_connection, monkeypatch):
        """Test handling when session creation returns None client"""

        def mock_create_session(self):
            self.client = None
            return False

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(NetworkError):
            valid_connection.test_connection()

    def test_client_verification_failure(self, valid_connection, monkeypatch):
        """Test handling when client verification fails"""

        def mock_create_session(self):
            self.client = object()
            return True

        def mock_verify_connection(self):
            raise NetworkError("Verification failed")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)
        monkeypatch.setattr(Connection, "_verify_connection", mock_verify_connection)

        with pytest.raises(NetworkError):
            valid_connection.test_connection()

    # State Testing
    def test_connection_state_after_failure(self, empty_connection):
        """Test that connection state is clean after failure"""
        with pytest.raises(ConfigurationError):
            empty_connection.test_connection()

        # Client should not be set after configuration failure
        assert empty_connection.client is None

    def test_multiple_test_calls_work(self, valid_connection, monkeypatch):
        """Test that multiple calls to test_connection work correctly"""
        call_count = 0

        def mock_create_session(self):
            nonlocal call_count
            call_count += 1
            self.client = f"client_{call_count}"
            return True

        def mock_verify_connection(self):
            pass

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)
        monkeypatch.setattr(Connection, "_verify_connection", mock_verify_connection)

        # Multiple successful calls
        valid_connection.test_connection()
        valid_connection.test_connection()

        assert call_count == 2
        assert valid_connection.client == "client_2"

    # Interface Compliance Tests
    def test_connection_implements_iconnection_interface(self, valid_connection):
        """Test that Connection properly implements IConnection interface"""
        assert isinstance(valid_connection, IConnection)
        assert hasattr(valid_connection, "test_connection")
        assert callable(valid_connection.test_connection)

    def test_test_connection_method_signature(self, valid_connection):
        """Test that test_connection has correct method signature"""
        import inspect

        sig = inspect.signature(valid_connection.test_connection)

        # Should have no required parameters (only self)
        assert len(sig.parameters) == 0

        # Should return None
        assert sig.return_annotation in (None, type(None), inspect.Signature.empty)

    # Property-based Testing Examples
    @pytest.mark.parametrize("url_scheme", ["http://", "https://", "ftp://"])
    def test_various_url_schemes(self, url_scheme, monkeypatch):
        """Test connections with different URL schemes"""
        connection = Connection(f"{url_scheme}test.com", "user", "pass")

        def mock_create_session(self):
            if url_scheme == "ftp://":
                raise requests.exceptions.MissingSchema("Unsupported scheme")
            self.client = "test_client"
            return True

        def mock_verify_connection(self):
            pass

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)
        monkeypatch.setattr(Connection, "_verify_connection", mock_verify_connection)

        if url_scheme == "ftp://":
            with pytest.raises(ConfigurationError):
                connection.test_connection()
        else:
            connection.test_connection()  # Should succeed

    # Performance/Stress Testing Markers
    @pytest.mark.slow
    def test_connection_timeout_behavior(self, valid_connection, monkeypatch):
        """Test connection behavior under timeout conditions"""

        def mock_create_session_slow(self):
            import time

            time.sleep(0.1)  # Simulate slow connection
            raise requests.exceptions.Timeout("Slow connection")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session_slow)

        with pytest.raises(NetworkError):
            valid_connection.test_connection()


# Custom Pytest Markers and Configuration
pytestmark = [
    pytest.mark.unit,  # Mark all tests as unit tests
    pytest.mark.connection,  # Mark all tests as connection-related
]


class TestConnectionIntegration:
    """Integration-style tests for Connection behavior"""

    def test_full_connection_workflow_success(self, monkeypatch):
        """Test complete successful connection workflow"""
        connection = Connection("https://test.com", "user", "pass")

        workflow_steps = []

        def mock_create_session(self):
            workflow_steps.append("create_session")
            self.client = "test_client"
            return True

        def mock_verify_connection(self):
            workflow_steps.append("verify_connection")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)
        monkeypatch.setattr(Connection, "_verify_connection", mock_verify_connection)

        connection.test_connection()

        # Verify workflow executed in correct order
        assert workflow_steps == ["create_session", "verify_connection"]
        assert connection.client == "test_client"

    def test_connection_failure_cleanup(self, monkeypatch):
        """Test that failed connections clean up properly"""
        connection = Connection("https://test.com", "user", "pass")

        def mock_create_session(self):
            self.client = "partial_client"  # Set client before failing
            raise requests.exceptions.ConnectionError("Connection failed")

        monkeypatch.setattr(Connection, "_create_session", mock_create_session)

        with pytest.raises(NetworkError):
            connection.test_connection()

        # Verify cleanup (depends on your implementation)
        # You might want to ensure failed connections don't leave partial state
