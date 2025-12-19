"""
Unit tests for Lambda handler.
"""

import json
from unittest.mock import Mock

import pytest

from src.lambda_handler import lambda_handler, process_request, validate_input


class TestLambdaHandler:
    """Test cases for lambda_handler function."""

    def test_lambda_handler_success(self) -> None:
        """Test successful lambda handler execution."""
        event = {"body": json.dumps({"name": "John"})}
        context = Mock()
        context.request_id = "test-request-id-123"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        assert "body" in response
        body = json.loads(response["body"])
        assert "message" in body
        assert "John" in body["message"]
        assert body["request_id"] == "test-request-id-123"

    def test_lambda_handler_with_dict_body(self) -> None:
        """Test lambda handler with dict body."""
        event = {"body": {"name": "Jane"}}
        context = Mock()
        context.request_id = "test-request-id-456"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "Jane" in body["message"]

    def test_lambda_handler_default_name(self) -> None:
        """Test lambda handler with missing name parameter."""
        event = {"body": json.dumps({})}
        context = Mock()
        context.request_id = "test-request-id-789"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "World" in body["message"]

    def test_lambda_handler_no_body(self) -> None:
        """Test lambda handler with no body."""
        event = {}
        context = Mock()
        context.request_id = "test-request-id-000"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "World" in body["message"]

    def test_lambda_handler_error(self) -> None:
        """Test lambda handler error handling."""
        event = {"body": json.dumps({"name": ""})}
        context = Mock()
        context.request_id = "test-request-id-error"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "error" in body

    def test_lambda_handler_invalid_json(self) -> None:
        """Test lambda handler with invalid JSON."""
        event = {"body": "invalid json"}
        context = Mock()
        context.request_id = "test-request-id-invalid"

        response = lambda_handler(event, context)

        assert response["statusCode"] == 500

    def test_lambda_handler_cors_headers(self) -> None:
        """Test that CORS headers are present."""
        event = {"body": json.dumps({"name": "Test"})}
        context = Mock()
        context.request_id = "test-cors"

        response = lambda_handler(event, context)

        assert "headers" in response
        assert "Access-Control-Allow-Origin" in response["headers"]
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"


class TestProcessRequest:
    """Test cases for process_request function."""

    def test_process_request_valid_name(self) -> None:
        """Test process_request with valid name."""
        result = process_request("Alice")
        assert "Alice" in result
        assert "Hello" in result

    def test_process_request_empty_string(self) -> None:
        """Test process_request with empty string."""
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            process_request("")

    def test_process_request_none(self) -> None:
        """Test process_request with None."""
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            process_request(None)  # type: ignore

    def test_process_request_non_string(self) -> None:
        """Test process_request with non-string input."""
        with pytest.raises(ValueError, match="Name must be a non-empty string"):
            process_request(123)  # type: ignore

    def test_process_request_special_characters(self) -> None:
        """Test process_request with special characters."""
        result = process_request("Test@123")
        assert "Test@123" in result


class TestValidateInput:
    """Test cases for validate_input function."""

    def test_validate_input_valid_dict(self) -> None:
        """Test validate_input with valid dictionary."""
        assert validate_input({"key": "value"}) is True

    def test_validate_input_empty_dict(self) -> None:
        """Test validate_input with empty dictionary."""
        assert validate_input({}) is True

    def test_validate_input_non_dict(self) -> None:
        """Test validate_input with non-dictionary input."""
        assert validate_input("not a dict") is False  # type: ignore
        assert validate_input(123) is False  # type: ignore
        assert validate_input(None) is False  # type: ignore

    def test_validate_input_nested_dict(self) -> None:
        """Test validate_input with nested dictionary."""
        nested = {"outer": {"inner": "value"}}
        assert validate_input(nested) is True


@pytest.fixture
def mock_context() -> Mock:
    """Fixture for mock Lambda context."""
    context = Mock()
    context.request_id = "test-request-id"
    context.function_name = "test-function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
    return context


def test_integration_full_flow(mock_context: Mock) -> None:
    """Integration test for full Lambda flow."""
    event = {"body": json.dumps({"name": "Integration Test"})}

    response = lambda_handler(event, mock_context)

    assert response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response

    body = json.loads(response["body"])
    assert "message" in body
    assert "Integration Test" in body["message"]
    assert body["request_id"] == "test-request-id"
