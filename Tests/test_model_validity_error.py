import pytest
from model.model_validity_error import ModelValidityError


class TestModelValidityErrorInitialization:
    """Test ModelValidityError initialization and basic properties"""

    def test_create_error_with_simple_message(self):
        """Test creating error with a simple string message"""
        message = "Test error message"
        error = ModelValidityError(message)

        assert error.message == message
        assert str(error) == message

    def test_create_error_with_empty_message(self):
        """Test creating error with empty message"""
        error = ModelValidityError("")

        assert error.message == ""
        assert str(error) == ""

    def test_create_error_with_none_message(self):
        """Test creating error with None message"""
        error = ModelValidityError(None)

        assert error.message is None
        assert str(error) == "None"

    def test_create_error_with_multiline_message(self):
        """Test creating error with multiline message"""
        message = "Line 1\nLine 2\nLine 3"
        error = ModelValidityError(message)

        assert error.message == message
        assert str(error) == message

    def test_create_error_with_unicode_message(self):
        """Test creating error with Unicode characters"""
        message = "Error: 用户输入无效 - тест"
        error = ModelValidityError(message)

        assert error.message == message
        assert str(error) == message

    def test_create_error_with_very_long_message(self):
        """Test creating error with very long message"""
        message = "x" * 10000
        error = ModelValidityError(message)

        assert error.message == message
        assert len(str(error)) == 10000

    def test_create_error_with_special_characters(self):
        """Test creating error with special characters"""
        message = "Error: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        error = ModelValidityError(message)

        assert error.message == message
        assert str(error) == message


class TestModelValidityErrorInheritance:
    """Test ModelValidityError inheritance and exception behavior"""

    def test_is_exception_subclass(self):
        """Test that ModelValidityError is a subclass of Exception"""
        assert issubclass(ModelValidityError, Exception)

    def test_is_exception_instance(self):
        """Test that ModelValidityError instances are Exception instances"""
        error = ModelValidityError("test")
        assert isinstance(error, Exception)
        assert isinstance(error, ModelValidityError)

    def test_can_be_raised_and_caught_as_exception(self):
        """Test that ModelValidityError can be raised and caught as Exception"""
        message = "Test exception"

        with pytest.raises(Exception) as exc_info:
            raise ModelValidityError(message)

        assert isinstance(exc_info.value, ModelValidityError)
        assert exc_info.value.message == message

    def test_can_be_raised_and_caught_specifically(self):
        """Test that ModelValidityError can be caught specifically"""
        message = "Specific test exception"

        with pytest.raises(ModelValidityError) as exc_info:
            raise ModelValidityError(message)

        assert exc_info.value.message == message
        assert str(exc_info.value) == message

    def test_exception_hierarchy(self):
        """Test the exception hierarchy"""
        error = ModelValidityError("test")

        # Should be an instance of its class hierarchy
        assert isinstance(error, ModelValidityError)
        assert isinstance(error, Exception)
        assert isinstance(error, BaseException)


class TestModelValidityErrorComparison:
    """Test ModelValidityError comparison and equality"""

    def test_equality_with_same_message(self):
        """Test that errors with same message are equal"""
        message = "Same message"
        error1 = ModelValidityError(message)
        error2 = ModelValidityError(message)

        # Note: Exception instances are not equal by default in Python
        # This tests the actual behavior, not necessarily desired behavior
        assert error1.message == error2.message
        assert str(error1) == str(error2)

    def test_inequality_with_different_messages(self):
        """Test that errors with different messages are not equal"""
        error1 = ModelValidityError("Message 1")
        error2 = ModelValidityError("Message 2")

        assert error1.message != error2.message
        assert str(error1) != str(error2)

    def test_message_comparison(self):
        """Test comparing error messages directly"""
        error1 = ModelValidityError("ABC")
        error2 = ModelValidityError("XYZ")

        assert error1.message < error2.message  # Alphabetical comparison
        assert error2.message > error1.message


class TestModelValidityErrorUsagePatterns:
    """Test common usage patterns for ModelValidityError"""

    def test_raise_with_context_message(self):
        """Test raising error with contextual information"""
        field_name = "user_id"
        invalid_value = "not-a-number"
        message = f"Invalid value '{invalid_value}' for field '{field_name}'"

        with pytest.raises(ModelValidityError) as exc_info:
            raise ModelValidityError(message)

        assert field_name in exc_info.value.message
        assert invalid_value in exc_info.value.message

    def test_raise_during_validation_scenario(self):
        """Test raising error in a validation scenario"""

        def validate_user_age(age):
            if age < 0:
                raise ModelValidityError(f"Age cannot be negative: {age}")
            if age > 150:
                raise ModelValidityError(f"Age seems unrealistic: {age}")
            return True

        # Valid age should not raise
        assert validate_user_age(25) is True

        # Invalid ages should raise with specific messages
        with pytest.raises(ModelValidityError) as exc_info:
            validate_user_age(-5)
        assert "cannot be negative" in exc_info.value.message

        with pytest.raises(ModelValidityError) as exc_info:
            validate_user_age(200)
        assert "unrealistic" in exc_info.value.message

    def test_chain_validation_errors(self):
        """Test chaining multiple validation errors"""

        def validate_note_data(note_data):
            errors = []

            if not note_data.get("content"):
                errors.append("Content is required")

            if note_data.get("type") not in ["abstract", "scope", "biography"]:
                errors.append("Invalid note type")

            if errors:
                raise ModelValidityError("; ".join(errors))

        # Valid data should not raise
        valid_data = {"content": "Some content", "type": "abstract"}
        validate_note_data(valid_data)  # Should not raise

        # Invalid data should raise with combined errors
        invalid_data = {"content": "", "type": "invalid"}
        with pytest.raises(ModelValidityError) as exc_info:
            validate_note_data(invalid_data)

        error_message = exc_info.value.message
        assert "Content is required" in error_message
        assert "Invalid note type" in error_message

    def test_error_in_class_method(self):
        """Test using ModelValidityError in a class validation method"""

        class MockNote:
            def __init__(self, content, note_type):
                self.content = content
                self.note_type = note_type

            def validate(self):
                if not self.content.strip():
                    raise ModelValidityError("Note content cannot be empty")

                if self.note_type not in ["abstract", "biography"]:
                    raise ModelValidityError(f"Unknown note type: {self.note_type}")

                return True

        # Valid note should validate successfully
        valid_note = MockNote("Valid content", "abstract")
        assert valid_note.validate() is True

        # Invalid notes should raise specific errors
        empty_note = MockNote("   ", "abstract")
        with pytest.raises(ModelValidityError) as exc_info:
            empty_note.validate()
        assert "cannot be empty" in exc_info.value.message

        invalid_type_note = MockNote("Content", "unknown")
        with pytest.raises(ModelValidityError) as exc_info:
            invalid_type_note.validate()
        assert "Unknown note type" in exc_info.value.message


class TestModelValidityErrorEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_error_with_numeric_message(self):
        """Test creating error with numeric message (converted to string)"""
        error = ModelValidityError(12345)

        assert error.message == 12345
        assert str(error) == "12345"

    def test_error_with_boolean_message(self):
        """Test creating error with boolean message"""
        error_true = ModelValidityError(True)
        error_false = ModelValidityError(False)

        assert error_true.message is True
        assert str(error_true) == "True"
        assert error_false.message is False
        assert str(error_false) == "False"

    def test_error_with_list_message(self):
        """Test creating error with list message"""
        message_list = ["Error 1", "Error 2", "Error 3"]
        error = ModelValidityError(message_list)

        assert error.message == message_list
        assert str(error) == str(message_list)

    def test_error_with_dict_message(self):
        """Test creating error with dictionary message"""
        message_dict = {"field": "value", "error": "invalid"}
        error = ModelValidityError(message_dict)

        assert error.message == message_dict
        assert str(error) == str(message_dict)

    def test_error_with_whitespace_only_message(self):
        """Test creating error with whitespace-only message"""
        whitespace_message = "   \t\n   "
        error = ModelValidityError(whitespace_message)

        assert error.message == whitespace_message
        assert str(error) == whitespace_message


class TestModelValidityErrorAttributes:
    """Test ModelValidityError attributes and methods"""

    def test_has_message_attribute(self):
        """Test that error has message attribute"""
        error = ModelValidityError("test")

        assert hasattr(error, "message")
        assert error.message == "test"

    def test_message_attribute_type(self):
        """Test that message attribute preserves type"""
        string_error = ModelValidityError("string")
        assert isinstance(string_error.message, str)

        int_error = ModelValidityError(42)
        assert isinstance(int_error.message, int)

        none_error = ModelValidityError(None)
        assert none_error.message is None

    def test_str_method_behavior(self):
        """Test __str__ method behavior"""
        test_cases = [
            ("Simple string", "Simple string"),
            ("", ""),
            (None, "None"),
            (42, "42"),
            ([1, 2, 3], "[1, 2, 3]"),
        ]

        for message, expected_str in test_cases:
            error = ModelValidityError(message)
            assert str(error) == expected_str

    def test_repr_method_behavior(self):
        """Test __repr__ method behavior (inherited from Exception)"""
        error = ModelValidityError("test message")
        repr_str = repr(error)

        # Should contain class name and message
        assert "ModelValidityError" in repr_str
        assert "test message" in repr_str


class TestModelValidityErrorInExceptionHandling:
    """Test ModelValidityError in various exception handling scenarios"""

    def test_multiple_exception_types(self):
        """Test catching ModelValidityError among other exception types"""

        def risky_operation(operation_type):
            if operation_type == "validity":
                raise ModelValidityError("Data is invalid")
            elif operation_type == "value":
                raise ValueError("Invalid value")
            elif operation_type == "type":
                raise TypeError("Wrong type")
            else:
                return "success"

        # Test catching specific exception
        with pytest.raises(ModelValidityError):
            risky_operation("validity")

        # Test catching different exception types
        with pytest.raises(ValueError):
            risky_operation("value")

        # Test successful operation
        assert risky_operation("normal") == "success"

    def test_exception_chaining(self):
        """Test exception chaining with ModelValidityError"""

        def inner_function():
            raise ValueError("Original error")

        def outer_function():
            try:
                inner_function()
            except ValueError as e:
                raise ModelValidityError("Validation failed due to inner error") from e

        with pytest.raises(ModelValidityError) as exc_info:
            outer_function()

        assert "Validation failed" in exc_info.value.message
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, ValueError)

    def test_finally_block_execution(self):
        """Test that finally blocks execute when ModelValidityError is raised"""
        cleanup_called = False

        def operation_with_cleanup():
            nonlocal cleanup_called
            try:
                raise ModelValidityError("Something went wrong")
            finally:
                cleanup_called = True

        with pytest.raises(ModelValidityError):
            operation_with_cleanup()

        assert cleanup_called is True


class TestModelValidityErrorDocumentation:
    """Test that ModelValidityError behaves as documented"""

    def test_docstring_example_usage(self):
        """Test usage patterns that might be in documentation"""

        # Example: Field validation
        def validate_field(field_name, value, constraints):
            if not value and constraints.get("required"):
                raise ModelValidityError(f"Field '{field_name}' is required")

            if isinstance(constraints.get("max_length"), int):
                if len(str(value)) > constraints["max_length"]:
                    raise ModelValidityError(
                        f"Field '{field_name}' exceeds maximum length of {constraints['max_length']}"
                    )

        # Should work with valid data
        validate_field("name", "John", {"required": True, "max_length": 50})

        # Should raise for missing required field
        with pytest.raises(ModelValidityError) as exc_info:
            validate_field("name", "", {"required": True})
        assert "is required" in exc_info.value.message

        # Should raise for too long value
        with pytest.raises(ModelValidityError) as exc_info:
            validate_field("name", "x" * 100, {"max_length": 50})
        assert "exceeds maximum length" in exc_info.value.message

    def test_integration_with_model_classes(self):
        """Test how ModelValidityError integrates with model validation"""

        class MockModel:
            def __init__(self, data):
                self.data = data

            def validate(self):
                errors = []

                if not self.data.get("id"):
                    errors.append("ID is required")

                if not self.data.get("name"):
                    errors.append("Name is required")

                if self.data.get("age") and self.data["age"] < 0:
                    errors.append("Age must be positive")

                if errors:
                    raise ModelValidityError(f"Validation failed: {'; '.join(errors)}")

                return True

        # Valid model should validate
        valid_model = MockModel({"id": 1, "name": "Test", "age": 25})
        assert valid_model.validate() is True

        # Invalid model should raise with all errors
        invalid_model = MockModel({"age": -5})
        with pytest.raises(ModelValidityError) as exc_info:
            invalid_model.validate()

        error_message = exc_info.value.message
        assert "ID is required" in error_message
        assert "Name is required" in error_message
        assert "Age must be positive" in error_message


class TestModelValidityErrorCompatibility:
    """Test ModelValidityError compatibility with different Python features"""

    def test_pickle_serialization(self):
        """Test that ModelValidityError can be pickled and unpickled"""
        import pickle

        original_error = ModelValidityError("Test error for pickling")

        # Serialize
        pickled_data = pickle.dumps(original_error)

        # Deserialize
        unpickled_error = pickle.loads(pickled_data)

        assert unpickled_error.message == original_error.message
        assert str(unpickled_error) == str(original_error)
        assert isinstance(unpickled_error, ModelValidityError)

    def test_with_logging(self):
        """Test ModelValidityError integration with logging"""
        import logging
        import io

        # Create a string buffer to capture log output
        log_buffer = io.StringIO()
        handler = logging.StreamHandler(log_buffer)
        logger = logging.getLogger("test_logger")
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

        try:
            raise ModelValidityError("Test error for logging")
        except ModelValidityError as e:
            logger.error("Caught validation error: %s", e)

        log_output = log_buffer.getvalue()
        assert "Test error for logging" in log_output
        assert "validation error" in log_output

    def test_with_json_serialization(self):
        """Test ModelValidityError message in JSON serialization contexts"""
        import json

        error = ModelValidityError("JSON serialization test")

        # Error message should be JSON serializable
        error_data = {
            "error_type": "ModelValidityError",
            "message": error.message,
            "timestamp": "2024-01-01T00:00:00Z",
        }

        json_string = json.dumps(error_data)
        parsed_data = json.loads(json_string)

        assert parsed_data["message"] == "JSON serialization test"
        assert parsed_data["error_type"] == "ModelValidityError"
