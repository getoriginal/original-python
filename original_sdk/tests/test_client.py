import os

import jwt
import pytest
from dotenv import load_dotenv

from original_sdk import Environment, OriginalClient

load_dotenv()

TEST_API_KEY = os.getenv("TEST_API_KEY")
TEST_API_SECRET = os.getenv("TEST_API_SECRET")

DEVELOPMENT_BASE_URL = "https://api-dev.getoriginal.com"
PRODUCTION_BASE_URL = "https://api.getoriginal.com"


class TestClient:
    def test_token(self, client: OriginalClient):
        token = client.token
        assert type(token) is str
        payload = jwt.decode(token, client.api_secret, algorithms=["HS256"])
        assert payload.get("api_key") == TEST_API_KEY

    def test_default_params(self, client: OriginalClient):
        assert client.get_default_params() == {
            "api_key": TEST_API_KEY,
            "api_secret": TEST_API_SECRET,
        }

    def test_default_base_url_is_production(self):
        client = OriginalClient(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET)
        assert client.base_url == PRODUCTION_BASE_URL

    def test_base_url_is_set(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            base_url="http://localhost:8000",
        )
        assert client.base_url == "http://localhost:8000"

    def test_base_url_removes_trailing_slashes(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            base_url="http://localhost:8000/",
        )
        assert client.base_url == "http://localhost:8000"

    def test_default_api_version(self):
        client = OriginalClient(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET)
        assert client.api_version == "v1"

    def test_api_version_is_set(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            api_version="v2",
        )
        assert client.api_version == "v2"

    def test_development_url_is_set_from_enum(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            env=Environment.Development,
        )
        assert client.base_url == DEVELOPMENT_BASE_URL

    def test_development_url_is_set_from_string(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            env="development",
        )
        assert client.base_url == DEVELOPMENT_BASE_URL

    def test_production_url_is_set_from_enum(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            env=Environment.Production,
        )
        assert client.base_url == PRODUCTION_BASE_URL

    def test_production_url_is_set_from_string(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            env="production",
        )
        assert client.base_url == PRODUCTION_BASE_URL

    def test_env_variable_overrides_default_development_url(self, monkeypatch):
        monkeypatch.setenv("ORIGINAL_ENV", "development")
        client = OriginalClient(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET)
        assert client.base_url == DEVELOPMENT_BASE_URL

    def test_env_variable_overrides_default_production_url(self, monkeypatch):
        monkeypatch.setenv("ORIGINAL_ENV", "production")
        client = OriginalClient(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET)
        assert client.base_url == PRODUCTION_BASE_URL

    def test_client_raises_error_if_bad_env_is_passed(self):
        with pytest.raises(ValueError) as ex:
            OriginalClient(
                api_key=TEST_API_KEY,
                api_secret=TEST_API_SECRET,
                env="bad_env",
            )
        assert "Invalid environment" in str(ex.value)

    def test_client_raises_error_if_bad_env_in_env_variables(self, monkeypatch):
        monkeypatch.setenv("ORIGINAL_ENV", "bad_env")
        with pytest.raises(ValueError) as ex:
            OriginalClient(
                api_key=TEST_API_KEY,
                api_secret=TEST_API_SECRET,
            )
        assert "Invalid environment" in str(ex.value)
