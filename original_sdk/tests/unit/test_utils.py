import string

import pytest

from original_sdk.utils import get_default_error_message, get_random_string


def test_random_string_length():
    length = 10
    random_string = get_random_string(length)
    assert (
        len(random_string) == length
    ), "The random string does not match the specified length"


def test_random_string_content():
    length = 100
    random_string = get_random_string(length)
    allowed_characters = string.ascii_letters + string.digits
    for char in random_string:
        assert (
            char in allowed_characters
        ), "The random string contains characters outside the allowed set"


def test_random_string_uniqueness():
    length = 10
    random_string_1 = get_random_string(length)
    random_string_2 = get_random_string(length)
    assert random_string_1 != random_string_2, (
        "Two consecutive calls to get_random_string produced the same output, "
        "which is highly unlikely for a properly functioning random generator"
    )


@pytest.mark.parametrize(
    "status_code, expected_message",
    [
        (200, "OK"),
        (404, "Not Found"),
        (500, "Internal Server Error"),
        (418, "I'm a Teapot"),
    ],
)
def test_get_default_error_message_valid_codes(status_code, expected_message):
    assert get_default_error_message(status_code) == expected_message


def test_get_default_error_message_unknown_code():
    invalid_status_code = 999
    assert get_default_error_message(invalid_status_code) == "Unknown Error"
