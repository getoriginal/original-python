import globals as gbl

from original_sdk import OriginalAsyncClient


class TestClientE2E:
    async def test_get_transfer_by_user_uid(self, async_client: OriginalAsyncClient):
        response = await async_client.get_transfers_by_user_uid(
            gbl.env_data["test_app_user_uid"]
        )
        assert isinstance(response["data"], list)
