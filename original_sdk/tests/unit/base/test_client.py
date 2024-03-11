from typing import Any, Union

import jwt
import pytest

from original_sdk.base.client import BaseOriginalClient
from original_sdk.types.environment import Environment
from original_sdk.types.exceptions import ClientError
from original_sdk.types.original_response import OriginalResponse

DEVELOPMENT_BASE_URL = "https://api-dev.getoriginal.com"
PRODUCTION_BASE_URL = "https://api.getoriginal.com"
DEFAULT_API_VERSION = "v1"


class MockClient(BaseOriginalClient):
    def create_user(
        self, email: Union[None, str] = None, client_id: Union[None, str] = None
    ):
        pass

    def get_user(self, uid: str):
        pass

    def get_user_by_email(self, email: str):
        pass

    def get_user_by_client_id(self, client_id: str):
        pass

    def get_collection(self, uid: str):
        pass

    def create_asset(self, **asset_data: Any):
        pass

    def edit_asset(self, uid: str, **asset_data: Any):
        pass

    def get_asset(self, uid: str):
        pass

    def get_assets_by_user_uid(self, user_uid: str):
        pass

    def create_transfer(self, **transfer_data: Any):
        pass

    def get_transfer(self, uid: str):
        pass

    def get_transfers_by_user_uid(self, user_uid: str):
        pass

    def create_burn(self, **burn_data: Any):
        pass

    def get_burn(self, uid: str):
        pass

    def get_burns_by_user_uid(self, user_uid: str):
        pass

    def get_deposit(self, user_uid: str):
        pass

    def get_reward(self, uid: str):
        pass

    def create_allocation(self, **allocation_data: Any):
        pass

    def get_allocation(self, uid: str):
        pass

    def get_allocations_by_user_uid(self, user_uid: str):
        pass

    def create_claim(self, **claim_data: Any):
        pass

    def get_claim(self, uid: str):
        pass

    def get_claims_by_user_uid(self, user_uid: str):
        pass


@pytest.fixture
def client(api_key="test_api_key", api_secret="test_api_secret", **options):
    return MockClient(api_key, api_secret, **options)


def test_constructor_uses_env_vars(monkeypatch):
    monkeypatch.setenv("ORIGINAL_TIMEOUT", "10")
    monkeypatch.setenv("ORIGINAL_URL", "https://customapi.getoriginal.com")
    monkeypatch.setenv("API_VERSION", "v2")

    client = MockClient("api_key", "api_secret")
    assert client.timeout == 10
    assert client.base_url == "https://customapi.getoriginal.com"
    assert client.env is None
    assert client.api_version == "v2"


def test_constructor_uses_env_vars_but_prioritised_env(monkeypatch):
    monkeypatch.setenv("ORIGINAL_TIMEOUT", "10")
    monkeypatch.setenv("ORIGINAL_URL", "https://customapi.getoriginal.com")
    monkeypatch.setenv("ORIGINAL_ENV", "development")
    monkeypatch.setenv("API_VERSION", "v2")

    client = MockClient("api_key", "api_secret")
    assert client.timeout == 10
    assert client.base_url == DEVELOPMENT_BASE_URL
    assert client.env == Environment.Development
    assert client.api_version == "v2"


def test_constructor_prioritizes_options_over_env_vars_with_monkeypatch(monkeypatch):
    monkeypatch.setenv("ORIGINAL_TIMEOUT", "10")
    monkeypatch.setenv("ORIGINAL_URL", "https://envapi.getoriginal.com")
    monkeypatch.setenv("API_VERSION", "v1")

    # Options explicitly set, overriding env vars
    options = {"base_url": "https://optionapi.getoriginal.com", "api_version": "v2"}
    client = MockClient("api_key", "api_secret", **options)

    assert client.timeout == 10
    assert client.base_url == "https://optionapi.getoriginal.com"
    assert client.env is None
    assert client.api_version == "v2"


def test_create_token(client):
    encoded_token = client.create_token()
    decoded_token = jwt.decode(encoded_token, client.api_secret, algorithms=["HS256"])
    assert decoded_token["api_key"] == client.api_key


def test_get_default_params(client):
    default_params = client.get_default_params()
    assert default_params == {
        "api_key": "test_api_key",
        "api_secret": "test_api_secret",
    }


def test_create_search_params(client):
    filter_conditions = {"status": "active"}
    query = "test query"
    search_params = client.create_search_params(filter_conditions, query)
    assert search_params["query"] == "test query"
    assert search_params["filter_conditions"] == filter_conditions

    # Test with dict query
    query_dict = {"type": "test_type"}
    search_params = client.create_search_params(filter_conditions, query_dict)
    assert search_params["message_filter_conditions"] == query_dict
    assert search_params["filter_conditions"] == filter_conditions


def test_handle_parsed_response_with_error_status_code(client):
    parsed_result = {
        "success": False,
        "error": {
            "type": "client_error",
            "detail": {"message": "An error occurred", "code": "error_code"},
        },
    }
    with pytest.raises(ClientError):
        client.handle_parsed_response(parsed_result, "Test error", 400, {})


def test_handle_parsed_response_with_success(client):
    parsed_result = {
        "success": True,
        "data": {"key": "value"},
    }
    response = client.handle_parsed_response(parsed_result, "Test success", 200, {})
    assert isinstance(response, OriginalResponse)
    assert response["data"] == parsed_result["data"]
