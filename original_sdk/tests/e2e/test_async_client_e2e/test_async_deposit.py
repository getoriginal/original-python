import globals as gbl

from original_sdk import OriginalAsyncClient


class TestAsyncClientDepositE2E:
    async def test_get_deposit(self, async_client: OriginalAsyncClient):
        user_uid = gbl.env_data["test_transfer_to_user_uid"]
        collection_uid = gbl.env_data["test_app_collection_uid"]
        response = await async_client.get_deposit(user_uid, collection_uid)
        assert response["data"]["chain_id"] == 80002
        assert response["data"]["network"] == "Amoy"
