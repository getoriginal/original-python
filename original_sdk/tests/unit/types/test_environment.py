import pytest

from original_sdk.types.environment import Environment, get_environment


def test_get_environment_with_enum_member():
    assert get_environment(Environment.Development) == Environment.Development
    assert get_environment(Environment.Production) == Environment.Production


def test_get_environment_with_valid_string():
    assert get_environment("development") == Environment.Development
    assert get_environment("production") == Environment.Production
    assert get_environment("DeVeLoPmEnT") == Environment.Development
    assert get_environment("PRODUCTION") == Environment.Production


def test_get_environment_with_invalid_string():
    with pytest.raises(ValueError) as exc_info:
        get_environment("invalid_env")
    assert "Invalid environment: invalid_env" in str(exc_info.value)
