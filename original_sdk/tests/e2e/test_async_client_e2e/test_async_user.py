import globals as gbl
import pytest

from original_sdk import ClientError, OriginalAsyncClient
from original_sdk.utils import get_random_string


class TestAsyncClientUserE2E:
    async def test_create_user_with_params(self, async_client: OriginalAsyncClient):
        user_external_id = get_random_string(8)
        response = await async_client.create_user(
            email=f"{user_external_id}@test.com", user_external_id=user_external_id
        )
        assert response["data"]["uid"] is not None

    async def test_create_user_with_deprecated_client_id(
        self, async_client: OriginalAsyncClient
    ):
        client_id = get_random_string(8)
        response = await async_client.create_user(
            email=f"{client_id}@test.com", client_id=client_id
        )
        assert response["data"]["uid"] is not None

    async def test_create_user_with_no_params(self, async_client: OriginalAsyncClient):
        response = await async_client.create_user()
        assert response["data"]["uid"] is not None

    async def test_error_message(self, async_client: OriginalAsyncClient):
        client_id = "existing_user"
        with pytest.raises(
            ClientError,
            match="'message': 'User already exists.'}",
        ):
            await async_client.create_user(
                email=f"{client_id}@test.com", client_id=client_id
            )

    async def test_get_user(self, multi_chain_client: OriginalAsyncClient):
        response = await multi_chain_client.get_user(
            gbl.env_data["test_transfer_to_user_uid"]
        )
        assert response["data"]["uid"] == gbl.env_data["test_transfer_to_user_uid"]
        assert response["data"]["wallets"] is not None
        assert (
            response["data"]["wallets"][0]["wallet_address"]
            == gbl.env_data["test_transfer_to_wallet_address"]
        )

    async def test_get_user_by_email(self, async_client: OriginalAsyncClient):
        response = await async_client.get_user_by_email(
            gbl.env_data["test_app_user_email"]
        )
        assert response["data"]["uid"] == gbl.env_data["test_app_user_uid"]
        assert response["data"]["email"] == gbl.env_data["test_app_user_email"]

    async def test_get_user_by_user_external_id(
        self, async_client: OriginalAsyncClient
    ):
        response = await async_client.get_user_by_user_external_id(
            gbl.env_data["test_app_user_client_id"]
        )
        assert response["data"]["uid"] == gbl.env_data["test_app_user_uid"]
        assert response["data"]["email"] == gbl.env_data["test_app_user_email"]

    async def test_get_user_by_client_id(self, async_client: OriginalAsyncClient):
        response = await async_client.get_user_by_client_id(
            gbl.env_data["test_app_user_client_id"]
        )
        assert response["data"]["uid"] == gbl.env_data["test_app_user_uid"]
        assert response["data"]["email"] == gbl.env_data["test_app_user_email"]

    async def test_get_user_by_client_id_with_no_results(
        self, async_client: OriginalAsyncClient
    ):
        response = await async_client.get_user_by_client_id("no_results")
        assert response["data"] is None

    async def test_get_user_not_found_throws_404(
        self, async_client: OriginalAsyncClient
    ):
        try:
            await async_client.get_user("not_found")
        except ClientError as e:
            assert e.status == 404
