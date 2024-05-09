import globals as gbl

from original_sdk import ClientError, OriginalAsyncClient


class TestClientE2E:
    async def test_get_collection(self, async_client: OriginalAsyncClient):
        response = await async_client.get_collection(
            gbl.env_data["test_app_collection_uid"]
        )
        assert response["data"]["uid"] == gbl.env_data["test_app_collection_uid"]

    async def test_get_collection_not_found_throws_404(
        self, async_client: OriginalAsyncClient
    ):
        try:
            await async_client.get_collection("not_found")
        except ClientError as e:
            assert e.status == 404
