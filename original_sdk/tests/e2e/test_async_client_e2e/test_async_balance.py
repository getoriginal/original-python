import globals as gbl

from original_sdk import ClientError, OriginalAsyncClient


class TestAsyncClientBalanceE2E:
    async def test_get_balance(self, async_client: OriginalAsyncClient):
        reward_uid = gbl.env_data["test_app_reward_uid"]
        user_uid = gbl.env_data["test_app_user_uid"]

        response = await async_client.get_balance(reward_uid, user_uid)
        assert response["data"]["reward_uid"] == reward_uid
        assert response["data"]["user_uid"] == user_uid
        assert isinstance(response["data"]["amount"], (int, float))

    async def test_get_balance_reward_not_found_throws_404(
        self, async_client: OriginalAsyncClient
    ):
        try:
            user_uid = gbl.env_data["test_app_user_uid"]
            await async_client.get_balance("not_found", user_uid)
        except ClientError as e:
            assert e.status == 404
