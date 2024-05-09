import globals as gbl

from original_sdk import ClientError, OriginalClient


class TestClientE2E:

    def test_get_reward(self, client: OriginalClient):
        response = client.get_reward(gbl.env_data["test_app_reward_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_app_reward_uid"]

    def test_get_reward_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_reward("not_found")
        except ClientError as e:
            assert e.status == 404