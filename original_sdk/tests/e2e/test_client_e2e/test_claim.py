import globals as gbl

from original_sdk import ClientError, OriginalClient


class TestClientE2E:
    def test_create_claim(self, client: OriginalClient):
        claim_data = {
            "reward_uid": gbl.env_data["test_app_reward_uid"],
            "from_user_uid": gbl.env_data["test_app_user_uid"],
            "to_address": gbl.env_data["test_claim_to_address"],
        }
        response = client.create_claim(**claim_data)
        assert response["data"]["uid"] is not None

    def test_get_claim(self, client: OriginalClient):
        response = client.get_claim(gbl.env_data["test_claim_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_claim_uid"]

    def test_get_claim_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_claim("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_get_claims_by_user_uid(self, client: OriginalClient):
        response = client.get_claims_by_user_uid(gbl.env_data["test_app_user_uid"])
        assert isinstance(response["data"], list)

    def test_get_claims_by_user_uid_with_no_results(self, client: OriginalClient):
        response = client.get_claims_by_user_uid("no_results")
        assert response["data"] == []
