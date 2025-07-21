import unittest
from unittest.mock import Mock
import json
import requests
from requests import Response
from requests.exceptions import ConnectionError, Timeout

# Import the classes we're testing
# Note: These imports assume the modules are available in the test environment
from Controller.ConnectionManager import ConnectionManager
from Controller.Connection import Connection
from Controller.HttpRequestType import HttpRequestType
from Controller.Interfaces import IQueryService


class TestConnectionManager(unittest.TestCase):
    """
    Comprehensive test suite for ConnectionManager class.
    Focuses on external behavior and contracts rather than implementation details.
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.connection_manager = ConnectionManager()
        # Mock only external dependencies, not internal methods
        self.mock_connection = Mock(spec=Connection)
        self.connection_manager.connection = self.mock_connection

    def tearDown(self):
        """Clean up after each test method."""
        self.connection_manager = None
        self.mock_connection = None


class TestConnectionManagerInitialization(TestConnectionManager):
    """Test ConnectionManager initialization and contract compliance."""

    def test_creates_connection_manager_instance(self):
        """Test that ConnectionManager can be instantiated."""
        cm = ConnectionManager()
        self.assertIsInstance(cm, ConnectionManager)

    def test_has_connection_attribute(self):
        """Test that ConnectionManager has a connection attribute."""
        cm = ConnectionManager()
        self.assertTrue(hasattr(cm, "connection"))
        self.assertIsInstance(cm.connection, Connection)

    def test_implements_query_service_interface(self):
        """Test that ConnectionManager implements IQueryService interface."""
        self.assertIsInstance(self.connection_manager, IQueryService)

        # Verify interface methods exist and are callable
        self.assertTrue(hasattr(self.connection_manager, "execute_query"))
        self.assertTrue(hasattr(self.connection_manager, "validate_query"))
        self.assertTrue(callable(getattr(self.connection_manager, "execute_query")))
        self.assertTrue(callable(getattr(self.connection_manager, "validate_query")))

    def test_accepts_connection_dependency(self):
        """Test that ConnectionManager can accept a connection dependency."""
        custom_connection = Mock(spec=Connection)
        cm = ConnectionManager()
        cm.connection = custom_connection

        self.assertIs(cm.connection, custom_connection)


class TestRepositoryRetrieval(TestConnectionManager):
    """Test repository retrieval behavior and contracts."""

    def test_get_repository_returns_repository_data(self):
        """Test that get_repository returns repository data for valid ID."""
        expected_data = {
            "uri": "/repositories/2",
            "repo_code": "TEST",
            "name": "Test Repository",
            "org_code": "TEST-ORG",
        }

        mock_response = Mock()
        mock_response.json = expected_data
        self.mock_connection.query.return_value = mock_response

        result = self.connection_manager.get_repository(2)

        # Test the contract: returns expected repository data
        self.assertEqual(result, expected_data)
        self.assertIsInstance(result, dict)

    def test_get_repository_calls_correct_endpoint(self):
        """Test that get_repository makes correct API call."""
        mock_response = Mock()
        mock_response.json = {"uri": "/repositories/2"}
        self.mock_connection.query.return_value = mock_response

        self.connection_manager.get_repository(2)

        # Verify the contract: correct endpoint is called
        self.mock_connection.query.assert_called_once_with(
            HttpRequestType.GET, "/repositories/2"
        )

    def test_get_repository_with_different_ids(self):
        """Test that get_repository works with different repository IDs."""
        test_cases = [2, 5, 10, 999]

        for repo_id in test_cases:
            with self.subTest(repo_id=repo_id):
                expected_data = {"uri": f"/repositories/{repo_id}"}
                mock_response = Mock()
                mock_response.json = expected_data
                self.mock_connection.query.return_value = mock_response

                result = self.connection_manager.get_repository(repo_id)

                self.assertEqual(result, expected_data)
                # Verify correct endpoint was called
                expected_call = (HttpRequestType.GET, f"/repositories/{repo_id}")
                self.assertIn(
                    expected_call,
                    [call.args for call in self.mock_connection.query.call_args_list],
                )

    def test_get_repository_propagates_connection_errors(self):
        """Test that connection errors are propagated to caller."""
        self.mock_connection.query.side_effect = ConnectionError("Network unreachable")

        with self.assertRaises(ConnectionError) as context:
            self.connection_manager.get_repository(2)

        # Verify error message is preserved for caller
        self.assertIn("Network unreachable", str(context.exception))

    def test_get_repository_propagates_timeout_errors(self):
        """Test that timeout errors are propagated to caller."""
        self.mock_connection.query.side_effect = Timeout("Request timed out")

        with self.assertRaises(Timeout) as context:
            self.connection_manager.get_repository(2)

        self.assertIn("Request timed out", str(context.exception))

    def test_get_repository_handles_json_decode_errors(self):
        """Test behavior when API returns invalid JSON."""
        mock_response = Mock()
        mock_response.json = Mock(
            side_effect=json.JSONDecodeError("Invalid JSON", "", 0)
        )
        self.mock_connection.query.return_value = mock_response

        with self.assertRaises(json.JSONDecodeError):
            self.connection_manager.get_repository(2)


class TestRepositoryListRetrieval(TestConnectionManager):
    """Test repository list retrieval behavior."""

    def test_get_repositories_returns_dictionary(self):
        """Test that get_repositories returns a dictionary of repositories."""
        # Mock sequential responses: repo 2, repo 3, then error (end of list)
        responses = [
            Mock(json=lambda: {"uri": "/repositories/2", "repo_code": "TEST1"}),
            Mock(json=lambda: {"uri": "/repositories/3", "repo_code": "TEST2"}),
            Mock(json=lambda: {"error": "Not found"}),
        ]

        self.mock_connection.query.side_effect = responses

        result = self.connection_manager.get_repositories()

        # Test the contract: returns dictionary
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertIn("/repositories/2", result)
        self.assertIn("/repositories/3", result)

    def test_get_repositories_starts_from_repo_2(self):
        """Test that repository scanning starts from repository 2."""
        mock_response = Mock()
        mock_response.json.return_value = {"error": "Not found"}
        self.mock_connection.query.return_value = mock_response

        self.connection_manager.get_repositories()

        # Verify first call is to repository 2
        first_call = self.mock_connection.query.call_args_list[0]
        self.assertEqual(first_call.args, (HttpRequestType.GET, "/repositories/2"))

    def test_get_repositories_stops_on_error(self):
        """Test that repository scanning stops when error is encountered."""
        # First repo exists, second returns error
        responses = [
            Mock(json=lambda: {"uri": "/repositories/2", "repo_code": "TEST"}),
            Mock(json=lambda: {"error": "Not found"}),
        ]

        self.mock_connection.query.side_effect = responses

        result = self.connection_manager.get_repositories()

        # Should only contain the first repository
        self.assertEqual(len(result), 1)
        self.assertIn("/repositories/2", result)

    def test_get_repositories_handles_empty_result(self):
        """Test behavior when no repositories exist."""
        mock_response = Mock()
        mock_response.json.return_value = {"error": "Not found"}
        self.mock_connection.query.return_value = mock_response

        result = self.connection_manager.get_repositories()

        # Should return empty dictionary
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_get_repositories_propagates_network_errors(self):
        """Test that network errors during repository listing are propagated."""
        self.mock_connection.query.side_effect = requests.exceptions.HTTPError(
            "500 Server Error"
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            self.connection_manager.get_repositories()


class TestResourceRetrieval(TestConnectionManager):
    """Test resource retrieval behavior."""

    def test_get_resource_record_returns_resource_data(self):
        """Test that get_resource_record returns resource data."""
        expected_data = {
            "uri": "/repositories/2/resources/1",
            "id_0": "TEST-001",
            "title": "Test Collection",
            "level": "collection",
        }

        mock_response = Mock()
        mock_response.json = expected_data
        self.mock_connection.query.return_value = mock_response

        result = self.connection_manager.get_resource_record(2, 1)

        # Test the contract: returns resource data
        self.assertEqual(result, expected_data)
        self.assertIsInstance(result, dict)

    def test_get_resource_record_calls_correct_endpoint(self):
        """Test that get_resource_record calls correct API endpoint."""
        mock_response = Mock()
        mock_response.json = {"uri": "/repositories/2/resources/1"}
        self.mock_connection.query.return_value = mock_response

        self.connection_manager.get_resource_record(2, 1)

        # Verify correct endpoint is called
        self.mock_connection.query.assert_called_once_with(
            HttpRequestType.GET, "/repositories/2/resources/1"
        )

    def test_get_resource_record_with_various_ids(self):
        """Test resource retrieval with different repository and resource IDs."""
        test_cases = [(2, 1), (3, 5), (10, 100), (999, 888)]

        for repo_id, resource_id in test_cases:
            with self.subTest(repo_id=repo_id, resource_id=resource_id):
                self.mock_connection.query.reset_mock()
                expected_uri = f"/repositories/{repo_id}/resources/{resource_id}"

                mock_response = Mock()
                mock_response.json = {"uri": expected_uri}
                self.mock_connection.query.return_value = mock_response

                result = self.connection_manager.get_resource_record(
                    repo_id, resource_id
                )

                self.assertEqual(result["uri"], expected_uri)
                self.mock_connection.query.assert_called_once_with(
                    HttpRequestType.GET, expected_uri
                )

    def test_get_resource_record_propagates_errors(self):
        """Test that errors during resource retrieval are propagated."""
        self.mock_connection.query.side_effect = ConnectionError("Connection failed")

        with self.assertRaises(ConnectionError):
            self.connection_manager.get_resource_record(2, 1)


class TestBatchResourceRetrieval(TestConnectionManager):
    """Test batch resource retrieval behavior."""

    def test_get_resource_records_returns_dictionary(self):
        """Test that get_resource_records returns dictionary of resources."""
        resource_ids = [1, 2, 3]

        # Mock get_resource_record to return different data for each ID
        def mock_get_resource(repo_id, resource_id):
            return {"uri": f"/repositories/{repo_id}/resources/{resource_id}"}

        # Replace the method with our mock
        original_method = self.connection_manager.get_resource_record
        self.connection_manager.get_resource_record = Mock(
            side_effect=mock_get_resource
        )

        try:
            result = self.connection_manager.get_resource_records(2, resource_ids)

            # Test the contract: returns dictionary with all requested resources
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 3)
            for resource_id in resource_ids:
                self.assertIn(resource_id, result)
        finally:
            # Restore original method
            self.connection_manager.get_resource_record = original_method

    def test_get_resource_records_calls_individual_retrieval(self):
        """Test that batch retrieval calls individual resource retrieval."""
        resource_ids = [1, 2]

        # Mock the individual get_resource_record method
        self.connection_manager.get_resource_record = Mock(
            return_value={"uri": "/repositories/2/resources/1"}
        )

        self.connection_manager.get_resource_records(2, resource_ids)

        # Verify individual retrieval was called for each resource
        self.assertEqual(self.connection_manager.get_resource_record.call_count, 2)

    def test_get_resource_records_handles_empty_list(self):
        """Test behavior with empty resource list."""
        result = self.connection_manager.get_resource_records(2, [])

        # Should return empty dictionary
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_get_resource_records_propagates_individual_errors(self):
        """Test that errors in individual resource retrieval are propagated."""
        resource_ids = [1, 999]  # Assume 999 will fail

        def mock_get_resource(repo_id, resource_id):
            if resource_id == 999:
                raise ValueError("Resource not found")
            return {"uri": f"/repositories/{repo_id}/resources/{resource_id}"}

        self.connection_manager.get_resource_record = Mock(
            side_effect=mock_get_resource
        )

        with self.assertRaises(ValueError):
            self.connection_manager.get_resource_records(2, resource_ids)


class TestResourceUpdate(TestConnectionManager):
    """Test resource update behavior."""

    def test_put_resource_record_returns_success_status(self):
        """Test that put_resource_record returns boolean success status."""
        resource_data = {
            "uri": "/repositories/2/resources/1",
            "title": "Updated Collection",
        }

        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200

        # Mock the client.put method
        self.mock_connection.client = Mock()
        self.mock_connection.client.put.return_value = mock_response

        result = self.connection_manager.put_resource_record(2, 1, resource_data)

        # Test the contract: returns boolean indicating success
        self.assertIsInstance(result, bool)
        self.assertTrue(result)

    def test_put_resource_record_calls_correct_endpoint(self):
        """Test that put_resource_record calls correct API endpoint."""
        resource_data = {"title": "Test Collection"}

        mock_response = Mock()
        mock_response.status_code = 200
        self.mock_connection.client = Mock()
        self.mock_connection.client.put.return_value = mock_response

        self.connection_manager.put_resource_record(2, 1, resource_data)

        # Verify correct endpoint and data
        self.mock_connection.client.put.assert_called_once_with(
            "/repositories/2/resources/1", json=resource_data
        )

    def test_put_resource_record_handles_client_errors(self):
        """Test behavior when update returns client error status."""
        resource_data = {"title": "Test Collection"}

        mock_response = Mock()
        mock_response.status_code = 400  # Client error
        self.mock_connection.client = Mock()
        self.mock_connection.client.put.return_value = mock_response

        result = self.connection_manager.put_resource_record(2, 1, resource_data)

        # Should return False for client errors
        self.assertFalse(result)

    def test_put_resource_record_handles_server_errors(self):
        """Test behavior when update returns server error status."""
        resource_data = {"title": "Test Collection"}

        mock_response = Mock()
        mock_response.status_code = 500  # Server error
        self.mock_connection.client = Mock()
        self.mock_connection.client.put.return_value = mock_response

        result = self.connection_manager.put_resource_record(2, 1, resource_data)

        # Should return False for server errors
        self.assertFalse(result)

    def test_put_resource_record_handles_connection_exceptions(self):
        """Test behavior when update raises connection exception."""
        resource_data = {"title": "Test Collection"}

        self.mock_connection.client = Mock()
        self.mock_connection.client.put.side_effect = ConnectionError("Network failed")

        result = self.connection_manager.put_resource_record(2, 1, resource_data)

        # Should return False when exception occurs
        self.assertFalse(result)

    def test_put_resource_record_with_various_endpoints(self):
        """Test update with different repository and resource combinations."""
        test_cases = [(2, 1), (3, 5), (10, 100)]
        resource_data = {"title": "Test"}

        for repo_id, resource_id in test_cases:
            with self.subTest(repo_id=repo_id, resource_id=resource_id):
                mock_response = Mock()
                mock_response.status_code = 200
                self.mock_connection.client = Mock()
                self.mock_connection.client.put.return_value = mock_response

                result = self.connection_manager.put_resource_record(
                    repo_id, resource_id, resource_data
                )

                self.assertTrue(result)
                expected_endpoint = f"/repositories/{repo_id}/resources/{resource_id}"
                self.mock_connection.client.put.assert_called_with(
                    expected_endpoint, json=resource_data
                )


class TestQueryServiceInterface(TestConnectionManager):
    """Test IQueryService interface contract compliance."""

    def test_execute_query_returns_response_object(self):
        """Test that execute_query returns Response object."""
        mock_query = Mock()

        result = self.connection_manager.execute_query(mock_query)

        # Test the contract: returns Response object
        self.assertIsInstance(result, Response)

    def test_execute_query_accepts_query_parameter(self):
        """Test that execute_query accepts query parameter without error."""
        mock_query = Mock()

        # Should not raise exception
        try:
            self.connection_manager.execute_query(mock_query)
        except Exception as e:
            self.fail(f"execute_query raised {type(e).__name__} unexpectedly: {e}")

    def test_validate_query_returns_boolean(self):
        """Test that validate_query returns boolean value."""
        mock_query = Mock()

        result = self.connection_manager.validate_query(mock_query)

        # Test the contract: returns boolean
        self.assertIsInstance(result, bool)

    def test_validate_query_handles_none_input(self):
        """Test that validate_query handles None input gracefully."""
        result = self.connection_manager.validate_query(None)

        # Should return boolean (likely False) rather than raise exception
        self.assertIsInstance(result, bool)

    def test_validate_query_with_various_inputs(self):
        """Test validate_query behavior with different input types."""
        test_inputs = [
            Mock(),  # Mock object
            {},  # Dictionary
            "",  # String
            123,  # Number
            [],  # List
        ]

        for test_input in test_inputs:
            with self.subTest(input_type=type(test_input).__name__):
                result = self.connection_manager.validate_query(test_input)
                # Should always return boolean, never raise exception
                self.assertIsInstance(result, bool)


class TestErrorPropagation(TestConnectionManager):
    """Test that errors are properly propagated to callers."""

    def test_network_errors_are_propagated(self):
        """Test that network-related errors are propagated unchanged."""
        error_types = [
            ConnectionError("Connection refused"),
            Timeout("Request timed out"),
            requests.exceptions.HTTPError("HTTP Error"),
        ]

        for error in error_types:
            with self.subTest(error_type=type(error).__name__):
                self.mock_connection.query.side_effect = error

                with self.assertRaises(type(error)) as context:
                    self.connection_manager.get_repository(2)

                # Error message should be preserved
                self.assertEqual(str(context.exception), str(error))

    def test_json_errors_are_propagated(self):
        """Test that JSON parsing errors are propagated."""
        mock_response = Mock()
        mock_response.json = Mock(
            side_effect=json.JSONDecodeError("Invalid JSON", "", 0)
        )
        self.mock_connection.query.return_value = mock_response

        with self.assertRaises(json.JSONDecodeError):
            self.connection_manager.get_repository(2)

    def test_unexpected_exceptions_are_propagated(self):
        """Test that unexpected exceptions are propagated."""
        self.mock_connection.query.side_effect = RuntimeError("Unexpected error")

        with self.assertRaises(RuntimeError) as context:
            self.connection_manager.get_repository(2)

        self.assertIn("Unexpected error", str(context.exception))


class TestDataConsistency(TestConnectionManager):
    """Test data consistency and state management."""

    def test_repeated_calls_return_consistent_results(self):
        """Test that repeated calls to same endpoint return consistent data."""
        expected_data = {"uri": "/repositories/2", "name": "Test Repo"}
        mock_response = Mock()
        mock_response.json = expected_data
        self.mock_connection.query.return_value = mock_response

        # Make multiple calls
        result1 = self.connection_manager.get_repository(2)
        result2 = self.connection_manager.get_repository(2)
        result3 = self.connection_manager.get_repository(2)

        # Results should be consistent
        self.assertEqual(result1, expected_data)
        self.assertEqual(result2, expected_data)
        self.assertEqual(result3, expected_data)
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)

    def test_different_parameters_call_different_endpoints(self):
        """Test that different parameters result in different API calls."""
        mock_response = Mock()
        mock_response.json = {"uri": "/repositories/2"}
        self.mock_connection.query.return_value = mock_response

        # Call with different repository IDs
        self.connection_manager.get_repository(2)
        self.connection_manager.get_repository(3)
        self.connection_manager.get_repository(5)

        # Verify different endpoints were called
        call_args = [call.args for call in self.mock_connection.query.call_args_list]
        expected_calls = [
            (HttpRequestType.GET, "/repositories/2"),
            (HttpRequestType.GET, "/repositories/3"),
            (HttpRequestType.GET, "/repositories/5"),
        ]

        for expected_call in expected_calls:
            self.assertIn(expected_call, call_args)

    def test_method_calls_do_not_affect_each_other(self):
        """Test that different method calls don't interfere with each other."""
        # Setup different responses for different methods
        repo_response = Mock()
        repo_response.json = {"uri": "/repositories/2"}

        resource_response = Mock()
        resource_response.json = {"uri": "/repositories/2/resources/1"}

        # Configure mock to return different responses based on endpoint
        def side_effect(method, endpoint):
            response = Mock()
            if "resources" in endpoint:
                response.json = resource_response.json
            else:
                response.json = repo_response.json
            return response

        self.mock_connection.query.side_effect = side_effect

        # Call different methods
        repo_result = self.connection_manager.get_repository(2)
        resource_result = self.connection_manager.get_resource_record(2, 1)

        # Results should be independent
        self.assertEqual(repo_result, {"uri": "/repositories/2"})
        self.assertEqual(resource_result, {"uri": "/repositories/2/resources/1"})


class TestEdgeCases(TestConnectionManager):
    """Test edge cases and boundary conditions."""

    def test_empty_response_handling(self):
        """Test behavior when API returns empty response."""
        mock_response = Mock()
        mock_response.json = {}  # Empty response
        self.mock_connection.query.return_value = mock_response

        result = self.connection_manager.get_repository(2)

        # Should return empty dict without error
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_large_repository_id_handling(self):
        """Test behavior with large repository IDs."""
        large_id = 999999
        expected_data = {"uri": f"/repositories/{large_id}"}

        mock_response = Mock()
        mock_response.json = expected_data
        self.mock_connection.query.return_value = mock_response

        result = self.connection_manager.get_repository(large_id)

        self.assertEqual(result, expected_data)

    def test_unicode_data_handling(self):
        """Test behavior with Unicode characters in response data."""
        unicode_data = {
            "uri": "/repositories/2",
            "name": "测试仓库",  # Chinese characters
            "description": "Тестовое описание",  # Cyrillic characters
        }

        mock_response = Mock()
        mock_response.json = unicode_data
        self.mock_connection.query.return_value = mock_response

        result = self.connection_manager.get_repository(2)

        # Should handle Unicode data correctly
        self.assertEqual(result, unicode_data)
        self.assertEqual(result["name"], "测试仓库")
        self.assertEqual(result["description"], "Тестовое описание")


# Integration tests (run only when integration environment is available)
class TestConnectionManagerIntegration(unittest.TestCase):
    """
    Integration tests for ConnectionManager with real ArchivesSpace API.
    These tests require a running ArchivesSpace instance.
    """

    @unittest.skipUnless(
        False,  # Set to True when integration environment is ready
        "Integration tests require live ArchivesSpace instance",
    )
    def setUp(self):
        """Set up integration test environment."""
        # These would be real connection parameters for integration testing
        self.connection_manager = ConnectionManager()
        # Would need to configure real connection here

    def test_real_repository_retrieval(self):
        """Test actual repository retrieval from live instance."""
        # This would test against a real ArchivesSpace instance
        # result = self.connection_manager.get_repository(2)
        # self.assertIsInstance(result, dict)
        # self.assertIn("uri", result)
        pass

    def test_real_error_conditions(self):
        """Test real error conditions with live API."""
        # This would test real error scenarios
        # with self.assertRaises(SomeExpectedError):
        #     self.connection_manager.get_repository(99999)
        pass


if __name__ == "__main__":
    # Create test suite excluding integration tests by default
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes except integration tests
    test_classes = [
        TestConnectionManagerInitialization,
        TestRepositoryRetrieval,
        TestRepositoryListRetrieval,
        TestResourceRetrieval,
        TestBatchResourceRetrieval,
        TestResourceUpdate,
        TestQueryServiceInterface,
        TestErrorPropagation,
        TestDataConsistency,
        TestEdgeCases,
        # TestConnectionManagerIntegration,  # Uncomment for integration tests
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)

    # Print summary
    print("\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = (
            (result.testsRun - len(result.failures) - len(result.errors))
            / result.testsRun
            * 100
        )
        print(f"Success rate: {success_rate:.1f}%")

    # Print any failures or errors
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
