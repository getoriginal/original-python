import globals as gbl

from original_sdk import ClientError, OriginalClient


class TestClientBalanceE2E:
    def test_get_balance(self, client: OriginalClient):
        reward_uid = gbl.env_data["test_app_reward_uid"]
        user_uid = gbl.env_data["test_app_user_uid"]
        response = client.get_balance(reward_uid, user_uid)
        assert response["data"]["reward_uid"] == gbl.env_data["test_app_reward_uid"]
        assert response["data"]["user_uid"] == gbl.env_data["test_app_user_uid"]
        assert isinstance(response["data"]["amount"], (int, float))

    def test_get_balance_reward_not_found_throws_404(self, client: OriginalClient):
        try:
            user_uid = gbl.env_data["test_app_user_uid"]

            client.get_balance("not_found", user_uid)
        except ClientError as e:
            assert e.status == 404
