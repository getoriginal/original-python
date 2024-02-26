import pytest

from original_sdk.types.exceptions import (
    ClientError,
    OriginalError,
    OriginalErrorCode,
    OriginalErrorData,
    ServerError,
    ValidationError,
    is_error_status_code,
    parse_and_raise_error,
)


def test_original_error():
    error_data: OriginalErrorData = {
        "success": False,
        "error": {
            "type": "client_error",
            "detail": {"message": "An error occurred", "code": "error_code"},
        },
    }
    error = OriginalError(
        "Error occurred", 400, error_data, OriginalErrorCode.client_error
    )
    assert "Error occurred - 400 - " in str(error)
    assert error.code == "client_error"


def test_client_error():
    error = ClientError("Client Error", 400, "Client error data")
    assert error.code == "client_error"


def test_server_error():
    error = ServerError("Server Error", 500, "Server error data")
    assert error.code == "server_error"


def test_validation_error():
    error = ValidationError("Validation Error", 422, "Validation error data")
    assert error.code == "validation_error"


def test_is_error_status_code():
    assert is_error_status_code(400)
    assert is_error_status_code(404)
    assert is_error_status_code(500)
    assert not is_error_status_code(200)
    assert not is_error_status_code(202)


def test_parse_and_raise_error_with_client_error():
    error_data = {
        "success": False,
        "error": {
            "type": "client_error",
            "detail": {"message": "Invalid request", "code": "invalid_request"},
        },
    }
    with pytest.raises(ClientError) as context:
        parse_and_raise_error(error_data, "Reason", 400)
    assert "Invalid request" == context.value.message
    assert 400 == context.value.status


def test_error_detail_as_single_dict():
    error_detail = {
        "message": "Single error message",
        "code": "single_error",
        "field_name": "field1",
    }
    error_data = {
        "success": False,
        "error": {"type": "client_error", "detail": error_detail},
    }
    with pytest.raises(ClientError) as context:
        parse_and_raise_error(error_data, "Single detail error", 400)
    assert "Single error message" in context.value.message
    assert 400 == context.value.status
    assert "client_error" == context.value.code


def test_error_detail_as_list():
    error_detail = [
        {
            "message": "First error message",
            "code": "first_error",
            "field_name": "field1",
        },
        {"message": "Second error message", "code": "second_error"},
    ]
    error_data = {
        "success": False,
        "error": {"type": "validation_error", "detail": error_detail},
    }
    with pytest.raises(ValidationError) as context:
        parse_and_raise_error(error_data, "Multiple validation errors", 422)
    assert "First error message" in context.value.message


def test_error_with_missing_fields():
    error_data = {
        "success": False,
        "error": {
            "type": "client_error",
            # Missing 'detail'
        },
    }
    with pytest.raises(ClientError) as context:
        parse_and_raise_error(error_data, "Missing fields", 400)
    assert "Missing fields" == context.value.message


def test_unexpected_error_type():
    error_data = {
        "success": False,
        "error": {
            "type": "unexpected_error_type",
            "detail": {
                "message": "An unexpected error occurred",
                "code": "unexpected",
            },
        },
    }

    with pytest.raises(OriginalError) as context:
        parse_and_raise_error(error_data, "Unexpected error type", 400)
    assert "An unexpected error occurred" in context.value.message
