import globals as gbl

from original_sdk import ClientError, OriginalAsyncClient


class TestClientE2E:
    async def test_get_reward(self, async_client: OriginalAsyncClient):
        response = await async_client.get_reward(gbl.env_data["test_app_reward_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_app_reward_uid"]

    async def test_get_reward_not_found_throws_404(
        self, async_client: OriginalAsyncClient
    ):
        try:
            await async_client.get_reward("not_found")
        except ClientError as e:
            assert e.status == 404
