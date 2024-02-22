from unittest import TestCase

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


class TestExceptions(TestCase):
    def test_original_error(self):
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
        self.assertIn("Error occurred - 400 - ", str(error))
        self.assertEqual(error.code, "client_error")

    def test_client_error(self):
        error = ClientError("Client Error", 400, "Client error data")
        self.assertEqual(error.code, "client_error")

    def test_server_error(self):
        error = ServerError("Server Error", 500, "Server error data")
        self.assertEqual(error.code, "server_error")

    def test_validation_error(self):
        error = ValidationError("Validation Error", 422, "Validation error data")
        self.assertEqual(error.code, "validation_error")

    def test_is_error_status_code(self):
        self.assertTrue(is_error_status_code(400))
        self.assertTrue(is_error_status_code(404))
        self.assertTrue(is_error_status_code(500))
        self.assertFalse(is_error_status_code(200))
        self.assertFalse(is_error_status_code(202))

    def test_parse_and_raise_error_with_client_error(self):
        error_data = {
            "success": False,
            "error": {
                "type": "client_error",
                "detail": {"message": "Invalid request", "code": "invalid_request"},
            },
        }
        with self.assertRaises(ClientError) as context:
            parse_and_raise_error(error_data, "Reason", 400)
        self.assertEqual("Invalid request", context.exception.message)
        self.assertEqual(400, context.exception.status)

    def test_error_detail_as_single_dict(self):
        error_detail = {
            "message": "Single error message",
            "code": "single_error",
            "field_name": "field1",
        }
        error_data = {
            "success": False,
            "error": {"type": "client_error", "detail": error_detail},
        }
        with self.assertRaises(ClientError) as context:
            parse_and_raise_error(error_data, "Single detail error", 400)
        self.assertIn("Single error message", context.exception.message)
        self.assertEqual(400, context.exception.status)
        self.assertEqual("client_error", context.exception.code)

    def test_error_detail_as_list(self):
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
        with self.assertRaises(ValidationError) as context:
            parse_and_raise_error(error_data, "Multiple validation errors", 422)
        self.assertIn("First error message", context.exception.message)

    def test_error_with_missing_fields(self):
        error_data = {
            "success": False,
            "error": {
                "type": "client_error",
                # Missing 'detail'
            },
        }
        with self.assertRaises(ClientError) as context:
            parse_and_raise_error(error_data, "Missing fields", 400)
        self.assertEqual("Missing fields", context.exception.message)

    def test_unexpected_error_type(self):
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

        with self.assertRaises(OriginalError) as context:
            parse_and_raise_error(error_data, "Unexpected error type", 400)
        self.assertIn("An unexpected error occurred", context.exception.message)

