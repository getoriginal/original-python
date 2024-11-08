import globals as gbl

from original_sdk import ClientError, OriginalClient
from original_sdk.utils import get_random_string


class TestAssetE2E:
    def test_create_asset(self, client: OriginalClient):
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
        response = client.create_asset(**request_data)
        assert response["data"]["uid"] is not None

    def test_create_asset_with_sale_price(self, client: OriginalClient):
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
            "sale_price_in_usd": 9.99,
        }
        response = client.create_asset(**request_data)
        assert response["data"]["uid"] is not None

    def test_get_asset(self, client: OriginalClient):
        response = client.get_asset(gbl.env_data["test_asset_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_asset_uid"]

    def test_get_asset_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_asset("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_get_asset_by_user_uid(self, client: OriginalClient):
        response = client.get_assets_by_user_uid(gbl.env_data["test_app_user_uid"])
        assert isinstance(response["data"], list)

    def test_get_asset_by_user_uid_with_no_results(self, client: OriginalClient):
        response = client.get_assets_by_user_uid("no_results")
        assert response["data"] == []
