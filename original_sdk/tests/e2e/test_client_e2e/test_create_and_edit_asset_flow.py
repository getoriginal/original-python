import time

import globals as gbl

from original_sdk import OriginalClient
from original_sdk.utils import get_random_string


class TestClientCreateAndEditAssetFlowE2E:
    def test_edit_asset(self, client: OriginalClient):
        asset_name = get_random_string(8)
        asset_data = {
            "name": asset_name,
            "unique_name": True,
            "image_url": "https://example.com/image.png",
            "store_image_on_ipfs": False,
            "description": "Asset description",
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
        asset_response = client.create_asset(**request_data)
        asset_uid = asset_response["data"]["uid"]
        is_transferable = False
        retries = 0

        while is_transferable is False and retries < gbl.env_data["test_retry_counter"]:
            response = client.get_asset(asset_uid)
            is_transferable = response["data"]["is_transferable"]
            if not is_transferable:
                time.sleep(15)
            retries += 1

        assert is_transferable, f"Asset {asset_uid} is not transferable."
        edited_data = {
            "data": {**asset_data, "description": "Asset description edited"}
        }
        edited_response = client.edit_asset(asset_uid, **edited_data)
        assert edited_response["success"] is True
