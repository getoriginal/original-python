from original_sdk.base.exceptions import OriginalAPIException


class TestExceptions:
    def test_exception_builds_from_valid_json(self):
        text = '{"success": false, "error": {"type": "client_error", "detail": {"code": "application_exception", "message": "Something went wrong. Please contact support."}}}'
        exception = OriginalAPIException(text, 400)
        assert exception.error_type == "client_error"
        assert exception.error_detail == {
            "code": "application_exception",
            "message": "Something went wrong. Please contact support.",
        }
        assert exception.status_code == 400
        assert exception.json_response is True
        assert (
            str(exception)
            == "Original error code 400: type: client_error: {'code': 'application_exception', 'message': 'Something went wrong. Please contact support.'}"
        )

    def test_exception_builds_from_invalid_json(self):
        # this is invalid json because of use of single quotes
        text = "{'success': False, 'error': {'type': 'client_error', 'detail': {'code': 'application_exception', 'message': 'Something went wrong. Please contact support.'}}}"
        exception = OriginalAPIException(text, 400)
        assert exception.status_code == 400
        assert exception.json_response is False
        assert str(exception) == "Original error HTTP code: 400"
