import globals as gbl

from original_sdk import ClientError, OriginalAsyncClient


class TestClientE2E:
    async def test_create_claim(self, async_client: OriginalAsyncClient):
        claim_data = {
            "reward_uid": gbl.env_data["test_app_reward_uid"],
            "from_user_uid": gbl.env_data["test_app_user_uid"],
            "to_address": gbl.env_data["test_claim_to_address"],
        }
        response = await async_client.create_claim(**claim_data)
        assert response["data"]["uid"] is not None

    async def test_get_claim(self, async_client: OriginalAsyncClient):
        response = await async_client.get_claim(gbl.env_data["test_claim_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_claim_uid"]

    async def test_get_claim_not_found_throws_404(
        self, async_client: OriginalAsyncClient
    ):
        try:
            await async_client.get_claim("not_found")
        except ClientError as e:
            assert e.status == 404

    async def test_get_claims_by_user_uid(self, async_client: OriginalAsyncClient):
        response = await async_client.get_claims_by_user_uid(
            gbl.env_data["test_app_user_uid"]
        )
        assert isinstance(response["data"], list)

    async def test_get_claims_by_user_uid_with_no_results(
        self, async_client: OriginalAsyncClient
    ):
        response = await async_client.get_claims_by_user_uid("no_results")
        assert response["data"] == []
