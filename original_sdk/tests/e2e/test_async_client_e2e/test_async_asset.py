import globals as gbl

from original_sdk import ClientError, OriginalAsyncClient
from original_sdk.utils import get_random_string


class TestAsyncClientAssetE2E:
    async def test_create_asset(self, async_client: OriginalAsyncClient):
        asset_name = get_random_string(8)
        asset_data = {
            "name": asset_name,
            "unique_name": True,
            "image_url": "https://example.com/image.png",
            "store_image_on_ipfs": False,
            "attributes": [
                {"trait_type": "Eyes", "value": "Green"},
                {"trait_type": "Hair", "value": "Black"},
            ],
        }
        request_data = {
            "data": asset_data,
            "user_uid": gbl.env_data["test_app_user_uid"],
            "asset_external_id": asset_name,
            "collection_uid": gbl.env_data["test_app_collection_uid"],
        }
        response = await async_client.create_asset(**request_data)
        assert response["data"]["uid"] is not None

    async def test_create_asset_with_mint_price(
        self, async_client: OriginalAsyncClient
    ):
        asset_name = get_random_string(8)
        asset_data = {
            "name": asset_name,
            "unique_name": True,
            "image_url": "https://example.com/image.png",
            "store_image_on_ipfs": False,
            "sale_price_in_usd": 9.99,
            "attributes": [
                {"trait_type": "Eyes", "value": "Green"},
                {"trait_type": "Hair", "value": "Black"},
            ],
        }
        request_data = {
            "data": asset_data,
            "user_uid": gbl.env_data["test_app_user_uid"],
            "asset_external_id": asset_name,
            "collection_uid": gbl.env_data["test_app_collection_uid"],
        }
        response = await async_client.create_asset(**request_data)
        assert response["data"]["uid"] is not None

    async def test_get_asset(self, async_client: OriginalAsyncClient):
        response = await async_client.get_asset(gbl.env_data["test_asset_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_asset_uid"]

    async def test_get_asset_not_found_throws_404(
        self, async_client: OriginalAsyncClient
    ):
        try:
            await async_client.get_asset("not_found")
        except ClientError as e:
            assert e.status == 404

    async def test_get_asset_by_user_uid(self, async_client: OriginalAsyncClient):
        response = await async_client.get_assets_by_user_uid(
            gbl.env_data["test_app_user_uid"]
        )
        assert isinstance(response["data"], list)

    async def test_get_asset_by_user_uid_with_no_results(
        self, async_client: OriginalAsyncClient
    ):
        response = await async_client.get_assets_by_user_uid("no_results")
        assert response["data"] == []
