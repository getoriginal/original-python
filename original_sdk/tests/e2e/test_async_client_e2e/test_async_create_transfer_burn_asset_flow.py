import time

import globals as gbl

from original_sdk import OriginalAsyncClient
from original_sdk.utils import get_random_string


class TestAsyncClientTransferBurnAssetFlowE2E:
    async def test_full_create_transfer_burn_asset_flow(
        self, async_client: OriginalAsyncClient
    ):
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
            "client_id": asset_name,
            "collection_uid": gbl.env_data["test_app_collection_uid"],
        }
        asset_response = await async_client.create_asset(**request_data)
        asset_uid = asset_response["data"]["uid"]
        is_transferable = False
        retries = 0

        while is_transferable is False and retries < gbl.env_data["test_retry_counter"]:
            response = await async_client.get_asset(asset_uid)
            is_transferable = response["data"]["is_transferable"]
            if not is_transferable:
                time.sleep(15)
            retries += 1

        assert is_transferable, f"Asset {asset_uid} is not transferable."

        transfer_response = await async_client.create_transfer(
            asset_uid=asset_uid,
            from_user_uid=gbl.env_data["test_app_user_uid"],
            to_address=gbl.env_data["test_transfer_to_wallet_address"],
        )
        assert transfer_response["success"] is True
        transfer_uid = transfer_response["data"]["uid"]
        is_transferring = True
        retries = 0

        while is_transferring is True and retries < gbl.env_data["test_retry_counter"]:
            response = await async_client.get_asset(asset_uid)
            is_transferring = response["data"]["is_transferring"]
            if is_transferring:
                time.sleep(15)
            retries += 1

        transfer_response = await async_client.get_transfer(transfer_uid)
        assert (
            transfer_response["success"] is True
        ), f"Transfer {transfer_uid} is not done."
        assert transfer_response["data"]["status"] == "done"

        transferred_asset = await async_client.get_asset(asset_uid)
        assert transferred_asset["data"]["is_transferable"] is True

        burn_response = await async_client.create_burn(
            asset_uid=asset_uid,
            from_user_uid=gbl.env_data["test_transfer_to_user_uid"],
        )
        assert burn_response["success"] is True
        burn_uid = burn_response["data"]["uid"]
        is_burning = True
        retries = 0

        while is_burning is True and retries < gbl.env_data["test_retry_counter"]:
            response = await async_client.get_burn(burn_uid)
            is_burning = response["data"]["status"] != "done"
            if is_burning:
                time.sleep(15)
            retries += 1

        burn_response = await async_client.get_burn(burn_uid)
        assert burn_response["success"] is True, f"Burn {burn_uid} is not done."
        assert burn_response["data"]["status"] == "done"

        final_asset_burned_status = False
        retries = 0

        while (
            final_asset_burned_status is False
            and retries < gbl.env_data["test_retry_counter"]
        ):
            response = await async_client.get_asset(asset_uid)
            final_asset_burned_status = response["data"]["is_burned"]
            if not final_asset_burned_status:
                time.sleep(15)
            retries += 1

        final_asset = await async_client.get_asset(asset_uid)
        assert final_asset["success"] is True, f"Asset {asset_uid} is not burned."
        assert final_asset["data"]["is_burned"] is True
