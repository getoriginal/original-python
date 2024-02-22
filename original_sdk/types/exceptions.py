from enum import Enum
from typing import List, Optional, TypedDict, Union


class ErrorDetail(TypedDict, total=False):
    message: str
    code: str
    field_name: Optional[str]


ErrorDetailList = List[ErrorDetail]


class Error(TypedDict):
    type: str
    detail: Union[ErrorDetail, ErrorDetailList]


class OriginalErrorData(TypedDict):
    success: bool
    error: Error


class OriginalErrorCode(Enum):
    client_error = "client_error"
    server_error = "server_error"
    validation_error = "validation_error"


class OriginalError(Exception):
    def __init__(
        self,
        message: str,
        status: int,
        data: Union[OriginalErrorData, str],
        code: OriginalErrorCode,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.data = data
        self.code = code.value

    def __str__(self) -> str:
        return f"{self.message} - {self.status} - {self.code} - {self.data}"


class ClientError(OriginalError):
    def __init__(
        self, message: str, status: int, data: Union[OriginalErrorData, str]
    ) -> None:
        super().__init__(message, status, data, OriginalErrorCode.client_error)


class ServerError(OriginalError):
    def __init__(
        self, message: str, status: int, data: Union[OriginalErrorData, str]
    ) -> None:
        super().__init__(message, status, data, OriginalErrorCode.server_error)


class ValidationError(OriginalError):
    def __init__(
        self, message: str, status: int, data: Union[OriginalErrorData, str]
    ) -> None:
        super().__init__(message, status, data, OriginalErrorCode.validation_error)


def is_error_status_code(status_code: int) -> bool:
    # Consider only client errors(400 - 499) and server errors(500 - 599) as errors.
    return status_code < 200 or status_code >= 400


def parse_and_raise_error(
    parsed_result: OriginalErrorData | str, reason: str, status: int
) -> None:
    error = parsed_result.get("error") if isinstance(parsed_result, dict) else None
    if error:
        error_type = error.get("type")
        detail = error.get("detail")
        if isinstance(detail, list):
            detail = detail[0]

        message = detail.get("message") if detail else reason

        if error_type == OriginalErrorCode.server_error.value:
            raise ServerError(message=message, status=status, data=parsed_result)
        elif error_type == OriginalErrorCode.validation_error.value:
            raise ValidationError(message=message, status=status, data=parsed_result)
        else:
            raise ClientError(message=message, status=status, data=parsed_result)
    else:
        raise ClientError(
            message="No error found in response when one was expected",
            status=status,
            data=parsed_result,
        )


OriginalAPIException = OriginalError
