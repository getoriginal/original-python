import string

from original_sdk.utils import get_random_string


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
