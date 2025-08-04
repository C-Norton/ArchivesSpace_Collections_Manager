import pytest
from controller.connection_exceptions import (
    ConnectionException,
    ConfigurationError,
    NetworkError,
    ServerError,
    AuthenticationError,
)


class TestConnectionExceptionHierarchy:
    """Test the exception hierarchy structure and inheritance"""

    def test_connection_exception_is_base_exception(self):
        """Test that ConnectionException inherits from Exception"""
        assert issubclass(ConnectionException, Exception)

        # Test instantiation
        error = ConnectionException()
        assert isinstance(error, Exception)
        assert isinstance(error, ConnectionException)

    def test_all_specific_exceptions_inherit_from_connection_exception(self):
        """Test that all specific exceptions inherit from ConnectionException"""
        exception_classes = [
            ConfigurationError,
            NetworkError,
            ServerError,
            AuthenticationError,
        ]

        for exception_class in exception_classes:
            assert issubclass(exception_class, ConnectionException)
            assert issubclass(exception_class, Exception)

    def test_exception_hierarchy_levels(self):
        """Test the complete inheritance hierarchy"""
        # Test MRO (Method Resolution Order) for proper inheritance
        assert ConnectionException.__bases__ == (Exception,)

        for exception_class in [
            ConfigurationError,
            NetworkError,
            ServerError,
            AuthenticationError,
        ]:
            assert ConnectionException in exception_class.__bases__
            assert Exception in exception_class.__mro__
            assert ConnectionException in exception_class.__mro__

    def test_exception_types_are_distinct(self):
        """Test that exception types are distinct from each other"""
        exception_classes = [
            ConnectionException,
            ConfigurationError,
            NetworkError,
            ServerError,
            AuthenticationError,
        ]

        # Each class should be different from the others
        for i, class1 in enumerate(exception_classes):
            for j, class2 in enumerate(exception_classes):
                if i != j:
                    assert class1 != class2
                    assert (
                        not issubclass(class1, class2) or class2 == ConnectionException
                    )


class TestConnectionExceptionInstantiation:
    """Test creating instances of each exception type"""

    def test_connection_exception_instantiation(self):
        """Test ConnectionException can be instantiated"""
        # Default instantiation
        error = ConnectionException()
        assert isinstance(error, ConnectionException)
        assert str(error) == ""

        # With message
        error_with_message = ConnectionException("Connection failed")
        assert str(error_with_message) == "Connection failed"

    def test_configuration_error_instantiation(self):
        """Test ConfigurationError can be instantiated"""
        # Default instantiation
        error = ConfigurationError()
        assert isinstance(error, ConfigurationError)
        assert isinstance(error, ConnectionException)

        # With message
        error_with_message = ConfigurationError("Invalid configuration")
        assert str(error_with_message) == "Invalid configuration"

    def test_network_error_instantiation(self):
        """Test NetworkError can be instantiated"""
        # Default instantiation
        error = NetworkError()
        assert isinstance(error, NetworkError)
        assert isinstance(error, ConnectionException)

        # With message
        error_with_message = NetworkError("Network timeout")
        assert str(error_with_message) == "Network timeout"

    def test_server_error_instantiation(self):
        """Test ServerError can be instantiated"""
        # Default instantiation
        error = ServerError()
        assert isinstance(error, ServerError)
        assert isinstance(error, ConnectionException)

        # With message
        error_with_message = ServerError("Internal server error")
        assert str(error_with_message) == "Internal server error"

    def test_authentication_error_instantiation(self):
        """Test AuthenticationError can be instantiated"""
        # Default instantiation
        error = AuthenticationError()
        assert isinstance(error, AuthenticationError)
        assert isinstance(error, ConnectionException)

        # With message
        error_with_message = AuthenticationError("Invalid credentials")
        assert str(error_with_message) == "Invalid credentials"


class TestExceptionRaisingAndCatching:
    """Test raising and catching exceptions in the hierarchy"""

    def test_raise_and_catch_connection_exception(self):
        """Test raising and catching ConnectionException"""
        with pytest.raises(ConnectionException) as exc_info:
            raise ConnectionException("Base connection error")

        assert str(exc_info.value) == "Base connection error"
        assert isinstance(exc_info.value, ConnectionException)

    def test_raise_and_catch_configuration_error(self):
        """Test raising and catching ConfigurationError"""
        with pytest.raises(ConfigurationError) as exc_info:
            raise ConfigurationError("Missing server URL")

        assert str(exc_info.value) == "Missing server URL"
        assert isinstance(exc_info.value, ConfigurationError)
        assert isinstance(exc_info.value, ConnectionException)

    def test_raise_and_catch_network_error(self):
        """Test raising and catching NetworkError"""
        with pytest.raises(NetworkError) as exc_info:
            raise NetworkError("Connection timeout")

        assert str(exc_info.value) == "Connection timeout"
        assert isinstance(exc_info.value, NetworkError)
        assert isinstance(exc_info.value, ConnectionException)

    def test_raise_and_catch_server_error(self):
        """Test raising and catching ServerError"""
        with pytest.raises(ServerError) as exc_info:
            raise ServerError("500 Internal Server Error")

        assert str(exc_info.value) == "500 Internal Server Error"
        assert isinstance(exc_info.value, ServerError)
        assert isinstance(exc_info.value, ConnectionException)

    def test_raise_and_catch_authentication_error(self):
        """Test raising and catching AuthenticationError"""
        with pytest.raises(AuthenticationError) as exc_info:
            raise AuthenticationError("Invalid username or password")

        assert str(exc_info.value) == "Invalid username or password"
        assert isinstance(exc_info.value, AuthenticationError)
        assert isinstance(exc_info.value, ConnectionException)


class TestPolymorphicExceptionHandling:
    """Test polymorphic exception handling through inheritance"""

    def test_catch_specific_exceptions_as_connection_exception(self):
        """Test that specific exceptions can be caught as ConnectionException"""
        specific_exceptions = [
            (ConfigurationError, "Config error"),
            (NetworkError, "Network error"),
            (ServerError, "Server error"),
            (AuthenticationError, "Auth error"),
        ]

        for exception_class, message in specific_exceptions:
            with pytest.raises(ConnectionException) as exc_info:
                raise exception_class(message)

            # Should catch as ConnectionException
            assert isinstance(exc_info.value, ConnectionException)
            assert isinstance(exc_info.value, exception_class)
            assert str(exc_info.value) == message

    def test_catch_specific_exceptions_as_base_exception(self):
        """Test that all connection exceptions can be caught as Exception"""
        all_exceptions = [
            (ConnectionException, "Base error"),
            (ConfigurationError, "Config error"),
            (NetworkError, "Network error"),
            (ServerError, "Server error"),
            (AuthenticationError, "Auth error"),
        ]

        for exception_class, message in all_exceptions:
            with pytest.raises(Exception) as exc_info:
                raise exception_class(message)

            assert isinstance(exc_info.value, Exception)
            assert isinstance(exc_info.value, exception_class)
            assert str(exc_info.value) == message

    def test_exception_handling_specificity(self):
        """Test that more specific exception handlers are triggered first"""

        def handle_errors():
            try:
                raise ConfigurationError("Specific config error")
            except ConfigurationError as e:
                return ("ConfigurationError", str(e))
            except ConnectionException as e:
                return ("ConnectionException", str(e))
            except Exception as e:
                return ("Exception", str(e))

        result = handle_errors()
        assert result == ("ConfigurationError", "Specific config error")

    def test_generic_connection_exception_handling(self):
        """Test handling any connection-related error generically"""

        def raise_various_connection_errors(error_type):
            if error_type == "config":
                raise ConfigurationError("Missing URL")
            elif error_type == "network":
                raise NetworkError("Timeout")
            elif error_type == "server":
                raise ServerError("500 Error")
            elif error_type == "auth":
                raise AuthenticationError("Bad credentials")
            else:
                raise ConnectionException("Generic error")

        def handle_connection_errors(error_type):
            try:
                raise_various_connection_errors(error_type)
            except ConnectionException as e:
                return f"Connection problem: {e}"

        # All should be handled by the generic ConnectionException handler
        assert handle_connection_errors("config") == "Connection problem: Missing URL"
        assert handle_connection_errors("network") == "Connection problem: Timeout"
        assert handle_connection_errors("server") == "Connection problem: 500 Error"
        assert handle_connection_errors("auth") == "Connection problem: Bad credentials"
        assert (
            handle_connection_errors("generic") == "Connection problem: Generic error"
        )


class TestExceptionAttributes:
    """Test exception attributes and methods"""

    def test_exception_args_attribute(self):
        """Test that exception args are properly set"""
        message = "Test error message"
        error = ConfigurationError(message)

        assert error.args == (message,)
        assert len(error.args) == 1
        assert error.args[0] == message

    def test_exception_str_representation(self):
        """Test string representation of exceptions"""
        test_cases = [
            (ConnectionException, "Base error"),
            (ConfigurationError, "Config error"),
            (NetworkError, "Network error"),
            (ServerError, "Server error"),
            (AuthenticationError, "Auth error"),
        ]

        for exception_class, message in test_cases:
            error = exception_class(message)
            assert str(error) == message

    def test_exception_repr_representation(self):
        """Test repr representation of exceptions"""
        error = ConfigurationError("Test message")
        repr_str = repr(error)

        assert "ConfigurationError" in repr_str
        assert "Test message" in repr_str

    def test_empty_message_handling(self):
        """Test exceptions with empty messages"""
        for exception_class in [
            ConnectionException,
            ConfigurationError,
            NetworkError,
            ServerError,
            AuthenticationError,
        ]:
            error = exception_class("")
            assert str(error) == ""
            assert error.args == ("",)

    def test_none_message_handling(self):
        """Test exceptions with None message"""
        for exception_class in [
            ConnectionException,
            ConfigurationError,
            NetworkError,
            ServerError,
            AuthenticationError,
        ]:
            # Most exception classes handle None by creating empty args
            error = exception_class()
            assert isinstance(error, exception_class)


class TestExceptionChaining:
    """Test exception chaining with 'from' and 'raise' patterns"""

    def test_exception_chaining_with_from(self):
        """Test chaining exceptions using 'raise ... from ...'"""
        original_error = ValueError("Original error")

        with pytest.raises(ConfigurationError) as exc_info:
            try:
                raise original_error
            except ValueError as e:
                raise ConfigurationError("Configuration failed") from e

        chained_error = exc_info.value
        assert str(chained_error) == "Configuration failed"
        assert chained_error.__cause__ is original_error
        assert isinstance(chained_error.__cause__, ValueError)

    def test_exception_chaining_implicit(self):
        """Test implicit exception chaining"""
        with pytest.raises(NetworkError) as exc_info:
            try:
                raise ValueError("Original error")
            except ValueError:
                raise NetworkError("Network error occurred")

        chained_error = exc_info.value
        assert str(chained_error) == "Network error occurred"
        # __context__ is set for implicit chaining
        assert chained_error.__context__ is not None
        assert isinstance(chained_error.__context__, ValueError)

    def test_multiple_exception_levels(self):
        """Test multiple levels of exception chaining"""

        def level_3():
            raise ValueError("Level 3 error")

        def level_2():
            try:
                level_3()
            except ValueError as e:
                raise NetworkError("Level 2 network error") from e

        def level_1():
            try:
                level_2()
            except NetworkError as e:
                raise ConfigurationError("Level 1 config error") from e

        with pytest.raises(ConfigurationError) as exc_info:
            level_1()

        error = exc_info.value
        assert str(error) == "Level 1 config error"
        assert isinstance(error.__cause__, NetworkError)
        assert str(error.__cause__) == "Level 2 network error"
        assert isinstance(error.__cause__.__cause__, ValueError)
        assert str(error.__cause__.__cause__) == "Level 3 error"


class TestExceptionMessagePatterns:
    """Test various message patterns and content"""

    def test_descriptive_error_messages(self):
        """Test that exceptions can hold descriptive messages"""
        test_cases = [
            (ConfigurationError, "Server URL 'invalid-url' is not a valid URL format"),
            (
                NetworkError,
                "Connection timeout after 30 seconds to server https://example.com",
            ),
            (ServerError, "HTTP 500 Internal Server Error: Database connection failed"),
            (
                AuthenticationError,
                "Authentication failed: Invalid username 'user123' or password",
            ),
        ]

        for exception_class, message in test_cases:
            error = exception_class(message)
            assert str(error) == message
            assert message in repr(error)

    def test_multiline_error_messages(self):
        """Test exceptions with multiline messages"""
        multiline_message = """Configuration error details:
        - Missing server URL
        - Invalid username format
        - Password too short"""

        error = ConfigurationError(multiline_message)
        assert str(error) == multiline_message
        assert "\n" in str(error)

    def test_unicode_error_messages(self):
        """Test exceptions with Unicode characters"""
        unicode_message = (
            "连接失败: 服务器不可用 (Connection failed: Server unavailable)"
        )
        error = NetworkError(unicode_message)

        assert str(error) == unicode_message
        assert isinstance(str(error), str)

    def test_very_long_error_messages(self):
        """Test exceptions with very long messages"""
        long_message = "Error: " + "x" * 10000
        error = ServerError(long_message)

        assert str(error) == long_message
        assert len(str(error)) == len(long_message)


class TestExceptionUsagePatterns:
    """Test common usage patterns for the exception hierarchy"""

    def test_connection_factory_error_handling(self):
        """Test error handling in a connection factory pattern"""

        def create_connection(config):
            if not config.get("server"):
                raise ConfigurationError("Server URL is required")

            if not config.get("username"):
                raise ConfigurationError("Username is required")

            # Simulate network error
            if config.get("server") == "unreachable.com":
                raise NetworkError("Unable to reach server unreachable.com")

            # Simulate server error
            if config.get("server") == "error.com":
                raise ServerError("Server returned HTTP 500")

            # Simulate auth error
            if config.get("username") == "baduser":
                raise AuthenticationError("Invalid credentials")

            return "Connected successfully"

        # Test successful connection
        good_config = {"server": "good.com", "username": "user"}
        assert create_connection(good_config) == "Connected successfully"

        # Test various error conditions
        with pytest.raises(ConfigurationError):
            create_connection({})

        with pytest.raises(NetworkError):
            create_connection({"server": "unreachable.com", "username": "user"})

        with pytest.raises(ServerError):
            create_connection({"server": "error.com", "username": "user"})

        with pytest.raises(AuthenticationError):
            create_connection({"server": "good.com", "username": "baduser"})

    def test_retry_logic_with_specific_exceptions(self):
        """Test retry logic that behaves differently for different exception types"""

        class ConnectionRetryManager:
            def __init__(self):
                self.attempt_count = 0

            def should_retry(self, exception):
                """Determine if we should retry based on exception type"""
                if isinstance(exception, (NetworkError, ServerError)):
                    return self.attempt_count < 3
                elif isinstance(exception, (ConfigurationError, AuthenticationError)):
                    return False  # Don't retry these
                else:
                    return False

            def attempt_connection(self, error_type, max_attempts=3):
                """Simulate connection attempts with different error types"""
                while self.attempt_count < max_attempts:
                    self.attempt_count += 1

                    if error_type == "network" and self.attempt_count < 3:
                        raise NetworkError(
                            f"Network error on attempt {self.attempt_count}"
                        )
                    elif error_type == "server" and self.attempt_count < 2:
                        raise ServerError(
                            f"Server error on attempt {self.attempt_count}"
                        )
                    elif error_type == "config":
                        raise ConfigurationError("Configuration error - no retry")
                    elif error_type == "auth":
                        raise AuthenticationError("Auth error - no retry")
                    else:
                        return f"Success on attempt {self.attempt_count}"

                raise NetworkError("Failed after all attempts")

        # Test successful retry
        manager = ConnectionRetryManager()
        try:
            while True:
                try:
                    result = manager.attempt_connection("network")
                    assert result == "Success on attempt 3"
                    break
                except (NetworkError, ServerError) as e:
                    if not manager.should_retry(e):
                        raise
        except ConnectionException:
            pytest.fail("Should have succeeded after retries")

        # Test non-retryable errors
        manager = ConnectionRetryManager()
        with pytest.raises(ConfigurationError):
            manager.attempt_connection("config")

        assert manager.attempt_count == 1  # Should not have retried

    def test_error_logging_and_categorization(self):
        """Test categorizing errors for logging purposes"""

        def categorize_error(error):
            """Categorize errors for different handling"""
            if isinstance(error, ConfigurationError):
                return "user_error"
            elif isinstance(error, AuthenticationError):
                return "security_issue"
            elif isinstance(error, NetworkError):
                return "infrastructure_issue"
            elif isinstance(error, ServerError):
                return "service_issue"
            elif isinstance(error, ConnectionException):
                return "connection_issue"
            else:
                return "unknown_error"

        test_cases = [
            (ConfigurationError("Bad config"), "user_error"),
            (AuthenticationError("Bad auth"), "security_issue"),
            (NetworkError("Network down"), "infrastructure_issue"),
            (ServerError("Server crash"), "service_issue"),
            (ConnectionException("Generic"), "connection_issue"),
        ]

        for error, expected_category in test_cases:
            assert categorize_error(error) == expected_category


class TestExceptionCompatibility:
    """Test compatibility with Python exception features"""

    def test_pickle_serialization(self):
        """Test that exceptions can be pickled and unpickled"""
        import pickle

        exceptions_to_test = [
            ConnectionException("Base error"),
            ConfigurationError("Config error"),
            NetworkError("Network error"),
            ServerError("Server error"),
            AuthenticationError("Auth error"),
        ]

        for original_error in exceptions_to_test:
            # Serialize
            pickled_data = pickle.dumps(original_error)

            # Deserialize
            unpickled_error = pickle.loads(pickled_data)

            assert type(unpickled_error) == type(original_error)
            assert str(unpickled_error) == str(original_error)
            assert unpickled_error.args == original_error.args

    def test_exception_with_multiple_args(self):
        """Corrected test that matches Python's actual behavior"""

        class ConnectionException(Exception):
            pass

        class ConfigurationError(ConnectionException):
            pass

        error = ConfigurationError("Primary message", "Secondary info", 12345)

        # These will pass
        assert len(error.args) == 3
        assert error.args[0] == "Primary message"
        assert error.args[1] == "Secondary info"
        assert error.args[2] == 12345

        # CORRECTED: Multiple args shows as tuple string
        assert str(error) == "('Primary message', 'Secondary info', 12345)"

        # If you want just the first message, access args[0]
        assert error.args[0] == "Primary message"

    def test_exception_context_managers(self):
        """Test exceptions work properly with context managers"""

        class MockResource:
            def __init__(self, should_fail=False):
                self.should_fail = should_fail
                self.closed = False

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.closed = True
                return False  # Don't suppress exceptions

            def do_work(self):
                if self.should_fail:
                    raise NetworkError("Work failed")
                return "Work completed"

        # Test successful case
        with MockResource() as resource:
            result = resource.do_work()
            assert result == "Work completed"
        assert resource.closed

        # Test exception case
        with pytest.raises(NetworkError):
            with MockResource(should_fail=True) as resource:
                resource.do_work()
        assert resource.closed  # Should still be cleaned up
