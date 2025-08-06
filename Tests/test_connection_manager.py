import json
import pytest
from unittest.mock import Mock
import requests
from requests.exceptions import ConnectionError, Timeout

# Import the classes we're testing
from controller.connection_manager import ConnectionManager
from controller.connection import Connection
from controller.HttpRequestType import HttpRequestType


@pytest.fixture
def mock_connection():
    """Create a mock connection for testing."""
    return Mock(spec=Connection)


@pytest.fixture
def connection_manager(mock_connection, mocker):
    """Create a ConnectionManager with mocked connection."""
    cm = ConnectionManager(mocker.Mock())
    cm.connection = mock_connection
    return cm


class TestConnectionManagerInitialization:
    """Test ConnectionManager initialization and contract compliance."""

    def test_creates_connection_manager_instance(self, mocker):
        """Test that ConnectionManager can be instantiated."""
        cm = ConnectionManager(mocker.Mock())
        assert isinstance(cm, ConnectionManager)

    def test_has_connection_attribute(self, mocker):
        """Test that ConnectionManager has a connection attribute."""
        cm = ConnectionManager(mocker.Mock())
        assert hasattr(cm, "connection")
        assert cm.connection is None

    def test_accepts_connection_dependency(self, mocker):
        """Test that ConnectionManager can accept a connection dependency."""
        custom_connection = Mock(spec=Connection)
        cm = ConnectionManager(mocker.Mock())
        cm.connection = custom_connection

        assert cm.connection is custom_connection


class TestRepositoryRetrieval:
    """Test repository retrieval behavior and contracts."""

    def test_get_repository_returns_repository_data(
        self, connection_manager, mock_connection
    ):
        """Test that get_repository returns repository data for valid ID."""
        expected_data = {
            "uri": "/repositories/2",
            "repo_code": "TEST",
            "name": "Test Repository",
            "org_code": "TEST-ORG",
        }

        # FIXED: Set json as JSON string, not dict
        mock_response = Mock()
        mock_response.json.return_value = json.dumps(expected_data)
        mock_connection.query.return_value = mock_response

        result = connection_manager.get_repository(2)

        # Test the contract: returns expected repository data
        assert result == json.dumps(expected_data)
        assert isinstance(result, str)

    def test_get_repository_calls_correct_endpoint(
        self, connection_manager, mock_connection
    ):
        """Test that get_repository makes correct API call."""
        mock_response = Mock()
        mock_response.json.return_value = json.dumps({"uri": "/repositories/2"})
        mock_connection.query.return_value = mock_response

        connection_manager.get_repository(2)

        # Verify the contract: correct endpoint is called
        mock_connection.query.assert_called_once_with(
            HttpRequestType.GET, "/repositories/2"
        )

    def test_get_repository_with_different_ids(
        self, connection_manager, mock_connection
    ):
        """Test that get_repository works with different repository IDs."""
        test_cases = [2, 5, 10, 999]

        for repo_id in test_cases:
            mock_connection.query.reset_mock()
            expected_data = {"uri": f"/repositories/{repo_id}"}
            mock_response = Mock()
            mock_response.json.return_value = json.dumps(expected_data)
            mock_connection.query.return_value = mock_response

            result = connection_manager.get_repository(repo_id)

            assert result == json.dumps(expected_data)
            # Verify correct endpoint was called
            expected_call = (HttpRequestType.GET, f"/repositories/{repo_id}")
            assert expected_call in [
                call.args for call in mock_connection.query.call_args_list
            ]

    def test_get_repository_propagates_connection_errors(
        self, connection_manager, mock_connection
    ):
        """Test that connection errors are propagated to caller."""
        mock_connection.query.side_effect = ConnectionError("Network unreachable")

        with pytest.raises(ConnectionError) as exc_info:
            connection_manager.get_repository(2)

        # Verify error message is preserved for caller
        assert "Network unreachable" in str(exc_info.value)

    def test_get_repository_propagates_timeout_errors(
        self, connection_manager, mock_connection
    ):
        """Test that timeout errors are propagated to caller."""
        mock_connection.query.side_effect = Timeout("Request timed out")

        with pytest.raises(Timeout) as exc_info:
            connection_manager.get_repository(2)

        assert "Request timed out" in str(exc_info.value)

    def test_get_repository_handles_json_decode_errors(
        self, connection_manager, mock_connection
    ):
        """Test behavior when API returns invalid JSON."""
        mock_response = Mock()
        # Set json as a string property that contains invalid JSON
        mock_response.json.return_value = (
            "invalid json string that will cause decode error"
        )
        mock_connection.query.return_value = mock_response
        with pytest.raises(json.JSONDecodeError):
            connection_manager.get_repository(2)


class TestRepositoryListRetrieval:
    """Test repository list retrieval behavior."""

    def test_get_repositories_returns_dictionary(
        self, connection_manager, mock_connection
    ):
        """Test that get_repositories returns a dictionary of repositories."""

        # Mock the response to return JSON strings
        mock_response = Mock()
        mock_response.content = '{"uri": "/repositories/2", "repo_code": "TEST1"}'

        mock_connection.query.return_value = mock_response

        result = connection_manager.get_repositories()

        assert isinstance(result, dict)
        assert result["uri"] == "/repositories/2"
        assert result["repo_code"] == "TEST1"

    def test_get_repositories_propagates_network_errors(
        self, connection_manager, mock_connection
    ):
        """Test that network errors during repository listing are propagated."""
        mock_connection.query.side_effect = requests.exceptions.HTTPError(
            "500 Server Error"
        )

        with pytest.raises(requests.exceptions.HTTPError):
            connection_manager.get_repositories()


class TestResourceRetrieval:
    """Test resource retrieval behavior."""

    def test_get_resource_record_returns_resource_data(
        self, connection_manager, mock_connection
    ):
        """Test that get_resource_record returns resource data."""
        expected_data = {
            "uri": "/repositories/2/resources/1",
            "id_0": "TEST-001",
            "title": "Test Collection",
            "level": "collection",
        }

        mock_response = Mock()
        mock_response.json.return_value = expected_data
        mock_connection.query.return_value = mock_response

        result = connection_manager.get_resource_record(2, 1)

        # Test the contract: returns resource data
        assert result == expected_data
        assert isinstance(result, dict)

    def test_get_resource_record_calls_correct_endpoint(
        self, connection_manager, mock_connection
    ):
        """Test that get_resource_record calls correct API endpoint."""
        mock_response = Mock()
        mock_response.json = {"uri": "/repositories/2/resources/1"}
        mock_connection.query.return_value = mock_response

        connection_manager.get_resource_record(2, 1)

        # Verify correct endpoint is called
        mock_connection.query.assert_called_once_with(
            HttpRequestType.GET, "/repositories/2/resources/1"
        )

    def test_get_resource_record_with_various_ids(
        self, connection_manager, mock_connection
    ):
        """Test resource retrieval with different repository and resource IDs."""
        test_cases = [(2, 1), (3, 5), (10, 100), (999, 888)]

        for repo_id, resource_id in test_cases:
            mock_connection.query.reset_mock()
            expected_uri = f"/repositories/{repo_id}/resources/{resource_id}"

            mock_response = Mock()
            mock_response.json.return_value = {"uri": expected_uri}
            mock_connection.query.return_value = mock_response

            result = connection_manager.get_resource_record(repo_id, resource_id)

            assert result["uri"] == expected_uri
            mock_connection.query.assert_called_once_with(
                HttpRequestType.GET, expected_uri
            )


class TestBatchResourceRetrieval:
    """Test batch resource retrieval behavior."""

    def test_get_resource_records_returns_dictionary(self, connection_manager):
        """Test that get_resource_records returns dictionary of resources."""
        resource_ids = [1, 2, 3]

        # Mock get_resource_record to return different data for each ID
        def mock_get_resource(repo_id, resource_id):
            return {"uri": f"/repositories/{repo_id}/resources/{resource_id}"}

        # Replace the method with our mock
        connection_manager.get_resource_record = Mock(side_effect=mock_get_resource)

        result = connection_manager.get_resource_records(2, resource_ids)

        # Test the contract: returns dictionary with all requested resources
        assert isinstance(result, dict)
        assert len(result) == 3
        for resource_id in resource_ids:
            assert resource_id in result

    def test_get_resource_records_calls_individual_retrieval(self, connection_manager):
        """Test that batch retrieval calls individual resource retrieval."""
        resource_ids = [1, 2]

        # Mock the individual get_resource_record method
        connection_manager.get_resource_record = Mock(
            return_value={"uri": "/repositories/2/resources/1"}
        )

        connection_manager.get_resource_records(2, resource_ids)

        # Verify individual retrieval was called for each resource
        assert connection_manager.get_resource_record.call_count == 2

    def test_get_resource_records_handles_empty_list(self, connection_manager):
        """Test behavior with empty resource list."""
        result = connection_manager.get_resource_records(2, [])

        # Should return empty dictionary
        assert result == {}
        assert isinstance(result, dict)

    def test_get_resource_records_propagates_individual_errors(
        self, connection_manager
    ):
        """Test that errors in individual resource retrieval are propagated."""
        resource_ids = [1, 999999]  # Assume 999999 will fail

        def mock_get_resource(repo_id, resource_id):
            if resource_id == 999999:
                raise ValueError("Resource not found")
            return {"uri": f"/repositories/{repo_id}/resources/{resource_id}"}

        connection_manager.get_resource_record = Mock(side_effect=mock_get_resource)

        with pytest.raises(ValueError):
            connection_manager.get_resource_records(2, resource_ids)


class TestResourceUpdate:
    """Test resource update behavior."""

    def test_put_resource_record_returns_success_status(
        self, connection_manager, mock_connection
    ):
        """Test that put_resource_record returns boolean success status."""
        resource_data = {
            "uri": "/repositories/2/resources/1",
            "title": "Updated Collection",
        }

        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200

        # Mock the client.put method
        mock_connection.client = Mock()
        mock_connection.client.put.return_value = mock_response

        result = connection_manager.put_resource_record(2, 1, resource_data)

        # Test the contract: returns boolean indicating success
        assert isinstance(result, bool)
        assert result is True

    def test_put_resource_record_calls_correct_endpoint(
        self, connection_manager, mock_connection
    ):
        """Test that put_resource_record calls correct API endpoint."""
        resource_data = {"title": "Test Collection"}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_connection.client = Mock()
        mock_connection.client.put.return_value = mock_response

        connection_manager.put_resource_record(2, 1, resource_data)

        # Verify correct endpoint and data
        mock_connection.client.put.assert_called_once_with(
            "/repositories/2/resources/1", json=resource_data
        )

    def test_put_resource_record_handles_client_errors(
        self, connection_manager, mock_connection
    ):
        """Test behavior when update returns client error status."""
        resource_data = {"title": "Test Collection"}

        mock_response = Mock()
        mock_response.status_code = 400  # Client error
        mock_connection.client = Mock()
        mock_connection.client.put.return_value = mock_response

        result = connection_manager.put_resource_record(2, 1, resource_data)

        # Should return False for client errors
        assert result is False

    def test_put_resource_record_handles_server_errors(
        self, connection_manager, mock_connection
    ):
        """Test behavior when update returns server error status."""
        resource_data = {"title": "Test Collection"}

        mock_response = Mock()
        mock_response.status_code = 500  # Server error
        mock_connection.client = Mock()
        mock_connection.client.put.return_value = mock_response

        result = connection_manager.put_resource_record(2, 1, resource_data)

        # Should return False for server errors
        assert result is False

    def test_put_resource_record_handles_connection_exceptions(
        self, connection_manager, mock_connection
    ):
        """Test behavior when update raises connection exception."""
        resource_data = {"title": "Test Collection"}

        mock_connection.client = Mock()
        mock_connection.client.put.side_effect = ConnectionError("Network failed")

        result = connection_manager.put_resource_record(2, 1, resource_data)

        # Should return False when exception occurs
        assert result is False

    def test_put_resource_record_with_various_endpoints(
        self, connection_manager, mock_connection
    ):
        """Test update with different repository and resource combinations."""
        test_cases = [(2, 1), (3, 5), (10, 100)]
        resource_data = {"title": "Test"}

        for repo_id, resource_id in test_cases:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_connection.client = Mock()
            mock_connection.client.put.return_value = mock_response

            result = connection_manager.put_resource_record(
                repo_id, resource_id, resource_data
            )

            assert result is True
            expected_endpoint = f"/repositories/{repo_id}/resources/{resource_id}"
            mock_connection.client.put.assert_called_with(
                expected_endpoint, json=resource_data
            )


class TestErrorPropagation:
    """Test that errors are properly propagated to callers."""

    def test_network_errors_are_propagated(self, connection_manager, mock_connection):
        """Test that network-related errors are propagated unchanged."""
        error_types = [
            ConnectionError("Connection refused"),
            Timeout("Request timed out"),
            requests.exceptions.HTTPError("HTTP Error"),
        ]

        for error in error_types:
            mock_connection.query.side_effect = error

            with pytest.raises(type(error)) as exc_info:
                connection_manager.get_repository(2)

            # Error message should be preserved
            assert str(exc_info.value) == str(error)

    def test_json_errors_are_propagated(self, connection_manager, mock_connection):
        """Test that JSON parsing errors are propagated."""
        mock_response = Mock()
        mock_response.json = Mock(
            side_effect=json.JSONDecodeError("Invalid JSON", "", 0)
        )
        mock_connection.query.return_value = mock_response
        with pytest.raises(json.JSONDecodeError):
            connection_manager.get_repository(2)

    def test_unexpected_exceptions_are_propagated(
        self, connection_manager, mock_connection
    ):
        """Test that unexpected exceptions are propagated."""
        mock_connection.query.side_effect = RuntimeError("Unexpected error")

        with pytest.raises(RuntimeError) as exc_info:
            connection_manager.get_repository(2)

        assert "Unexpected error" in str(exc_info.value)


class TestDataConsistency:
    """Test data consistency and state management."""

    def test_repeated_calls_return_consistent_results(
        self, connection_manager, mock_connection
    ):
        """Test that repeated calls to same endpoint return consistent data."""
        expected_data = {"uri": "/repositories/2", "name": "Test Repo"}
        mock_response = Mock()
        mock_response.json.return_value = json.dumps(expected_data)
        mock_connection.query.return_value = mock_response

        # Make multiple calls
        result1 = connection_manager.get_repository(2)
        result2 = connection_manager.get_repository(2)
        result3 = connection_manager.get_repository(2)

        # Results should be consistent
        expected_json = json.dumps(expected_data)
        assert result1 == expected_json
        assert result2 == expected_json
        assert result3 == expected_json
        assert result1 == result2 == result3

    def test_different_parameters_call_different_endpoints(
        self, connection_manager, mock_connection
    ):
        """Test that different parameters result in different API calls."""
        mock_response = Mock()
        mock_response.json.return_value = json.dumps({"uri": "/repositories/2"})
        mock_connection.query.return_value = mock_response

        # Call with different repository IDs
        connection_manager.get_repository(2)
        connection_manager.get_repository(3)
        connection_manager.get_repository(5)

        # Verify different endpoints were called
        call_args = [call.args for call in mock_connection.query.call_args_list]
        expected_calls = [
            (HttpRequestType.GET, "/repositories/2"),
            (HttpRequestType.GET, "/repositories/3"),
            (HttpRequestType.GET, "/repositories/5"),
        ]

        for expected_call in expected_calls:
            assert expected_call in call_args

    def test_method_calls_do_not_affect_each_other(
        self, connection_manager, mock_connection
    ):
        """Test that different method calls don't interfere with each other."""
        # Setup different responses for different methods
        repo_response_data = {"uri": "/repositories/2"}
        resource_response_data = {"uri": "/repositories/2/resources/1"}

        # Configure mock to return different responses based on endpoint
        def side_effect(method, endpoint):
            response = Mock()
            if "resources" in endpoint:
                response.json.return_value = resource_response_data
            else:
                response.json.return_value = json.dumps(repo_response_data)
            return response

        mock_connection.query.side_effect = side_effect

        # Call different methods
        repo_result = connection_manager.get_repository(2)
        resource_result = connection_manager.get_resource_record(2, 1)

        # Results should be independent
        assert repo_result == json.dumps(repo_response_data)
        assert resource_result == resource_response_data


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_response_handling(self, connection_manager, mock_connection):
        """Test behavior when API returns empty response."""
        mock_response = Mock()
        mock_response.json.return_value = json.dumps(
            {}
        )  # Empty response as JSON string
        mock_connection.query.return_value = mock_response

        result = connection_manager.get_repository(2)

        # Should return empty dict as JSON string without error
        assert result == json.dumps({})
        assert isinstance(result, str)

    def test_large_repository_id_handling(self, connection_manager, mock_connection):
        """Test behavior with large repository IDs."""
        large_id = 999999
        expected_data = {"uri": f"/repositories/{large_id}"}

        mock_response = Mock()
        mock_response.json.return_value = json.dumps(expected_data)
        mock_connection.query.return_value = mock_response

        result = connection_manager.get_repository(large_id)

        assert result == json.dumps(expected_data)

    def test_unicode_data_handling(self, connection_manager, mock_connection):
        """Test behavior with Unicode characters in response data."""
        unicode_data = {
            "uri": "/repositories/2",
            "name": "测试仓库",  # Chinese characters
            "description": "Тестовое описание",  # Cyrillic characters
        }

        mock_response = Mock()
        mock_response.json.return_value = json.dumps(unicode_data, ensure_ascii=False)
        mock_connection.query.return_value = mock_response

        result = connection_manager.get_repository(2)

        # Should handle Unicode data correctly
        assert result == json.dumps(unicode_data, ensure_ascii=False)


# Integration tests (marked with pytest.mark.integration)
@pytest.mark.integration
class TestConnectionManagerIntegration:
    """
    Integration tests for ConnectionManager with real ArchivesSpace API.
    These tests require a running ArchivesSpace instance.
    """

    @pytest.fixture
    def real_connection_manager(self):
        """Set up integration test environment."""
        # These would be real connection parameters for integration testing
        return ConnectionManager()
        # Would need to configure real connection here

    @pytest.mark.skip(reason="Integration tests require live ArchivesSpace instance")
    def test_real_repository_retrieval(self, real_connection_manager):
        """Test actual repository retrieval from live instance."""
        # This would test against a real ArchivesSpace instance
        # result = real_connection_manager.get_repository(2)
        # assert isinstance(result, str)
        # assert "uri" in json.loads(result)
        pass

    @pytest.mark.skip(reason="Integration tests require live ArchivesSpace instance")
    def test_real_error_conditions(self, real_connection_manager):
        """Test real error conditions with live API."""
        # This would test real error scenarios
        # with pytest.raises(SomeExpectedError):
        #     real_connection_manager.get_repository(99999)
        pass
