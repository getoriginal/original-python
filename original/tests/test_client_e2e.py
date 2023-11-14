import os

from dotenv import load_dotenv

from original import Original
from original.tests.utils import get_random_string
import time

load_dotenv()

TEST_APP_USER_EMAIL = os.getenv('TEST_APP_USER_EMAIL')
TEST_APP_USER_UID = os.getenv('TEST_APP_USER_UID')
TEST_APP_USER_CLIENT_ID = os.getenv('TEST_APP_USER_CLIENT_ID')
TEST_APP_COLLECTION_UID = os.getenv('TEST_APP_COLLECTION_UID')
TEST_ASSET_UID = os.getenv('TEST_ASSET_UID')
TEST_TRANSFER_TO_WALLET_ADDRESS = os.getenv('TEST_TRANSFER_TO_WALLET_ADDRESS')
TEST_TRANSFER_TO_USER_UID = os.getenv('TEST_TRANSFER_TO_USER_UID')


class TestClient:

    def test_create_user(self, client: Original):
        client_id = get_random_string(8)
        response = client.create_user(email=f"{client_id}@test.com", client_id=client_id)
        assert response["data"]["uid"] is not None

    def test_get_user(self, client: Original):
        response = client.get_user(TEST_APP_USER_UID)
        assert response["data"]["uid"] == TEST_APP_USER_UID
        assert response["data"]["email"] == TEST_APP_USER_EMAIL

    def test_get_user_by_email(self, client: Original):
        response = client.get_user_by_email(TEST_APP_USER_EMAIL)
        assert response["data"]["uid"] == TEST_APP_USER_UID
        assert response["data"]["email"] == TEST_APP_USER_EMAIL

    def test_get_user_by_client_id(self, client: Original):
        response = client.get_user_by_client_id(TEST_APP_USER_CLIENT_ID)
        assert response["data"]["uid"] == TEST_APP_USER_UID
        assert response["data"]["email"] == TEST_APP_USER_EMAIL

    def test_get_user_by_client_id_with_no_results(self, client: Original):
        response = client.get_user_by_client_id("no_results")
        assert response["data"] == None

    def test_get_user_not_found_throws_404(self, client: Original):
        try:
            client.get_user("not_found")
        except Exception as e:
            assert e.status_code == 404

    def test_get_collection(self, client: Original):
        response = client.get_collection(TEST_APP_COLLECTION_UID)
        assert response["data"]["uid"] == TEST_APP_COLLECTION_UID

    def test_get_collection_not_found_throws_404(self, client: Original):
        try:
            client.get_collection("not_found")
        except Exception as e:
            assert e.status_code == 404

    def test_create_asset(self, client: Original):
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
            "user_uid": TEST_APP_USER_UID,
            "client_id": asset_name,
            "collection_uid": TEST_APP_COLLECTION_UID,
        }
        response = client.create_asset(**request_data)
        assert response["data"]["uid"] is not None

    def test_edit_asset(self, client: Original):
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
            "user_uid": TEST_APP_USER_UID,
            "client_id": asset_name,
            "collection_uid": TEST_APP_COLLECTION_UID,
        }
        asset_response = client.create_asset(**request_data)
        asset_uid = asset_response["data"]["uid"]
        is_transferable = False
        retries = 0

        while is_transferable is False and retries < 10:
            response = client.get_asset(asset_uid)
            is_transferable = response["data"]["is_transferable"]
            time.sleep(15)
            retries += 1

        assert is_transferable is True
        edited_data = {"data": {**asset_data, "description": "Asset description edited"}}
        edited_response = client.edit_asset(asset_uid, **edited_data)
        assert edited_response["success"] is True

    def test_get_asset(self, client: Original):
        response = client.get_asset(TEST_ASSET_UID)
        assert response["data"]["uid"] == TEST_ASSET_UID

    def test_get_asset_not_found_throws_404(self, client: Original):
        try:
            client.get_asset("not_found")
        except Exception as e:
            assert e.status_code == 404

    def test_get_asset_by_user_uid(self, client: Original):
        response = client.get_assets_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_get_asset_by_user_uid_with_no_results(self, client: Original):
        response = client.get_assets_by_user_uid("no_results")
        assert response["data"] == []

    def test_get_transfer_by_user_uid(self, client: Original):
        response = client.get_transfers_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_get_burn_by_user_uid(self, client: Original):
        response = client.get_burns_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_full_create_transfer_burn_asset_flow(self, client: Original):
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
            "user_uid": TEST_APP_USER_UID,
            "client_id": asset_name,
            "collection_uid": TEST_APP_COLLECTION_UID,
        }
        asset_response = client.create_asset(**request_data)
        asset_uid = asset_response["data"]["uid"]
        is_transferable = False
        retries = 0

        while is_transferable is False and retries < 10:
            response = client.get_asset(asset_uid)
            is_transferable = response["data"]["is_transferable"]
            time.sleep(15)
            retries += 1

        assert is_transferable is True
        transfer_response = client.create_transfer(
            asset_uid=asset_uid,
            from_user_uid=TEST_APP_USER_UID,
            to_address=TEST_TRANSFER_TO_WALLET_ADDRESS,
        )
        assert transfer_response["success"] is True
        transfer_uid = transfer_response["data"]["uid"]
        is_transferring = True
        retries = 0

        while is_transferring is True and retries < 10:
            response = client.get_asset(asset_uid)
            is_transferring = response["data"]["is_transferring"]
            time.sleep(15)
            retries += 1

        transfer_response = client.get_transfer(transfer_uid)
        assert transfer_response["success"] is True
        assert transfer_response["data"]["status"] == 'done'

        transferred_asset = client.get_asset(asset_uid)
        assert transferred_asset["data"]["is_transferable"] is True

        burn_response = client.create_burn(
            asset_uid=asset_uid,
            from_user_uid=TEST_TRANSFER_TO_USER_UID,
        )
        assert burn_response["success"] is True
        burn_uid = burn_response["data"]["uid"]
        is_burning = True
        retries = 0

        while is_burning is True and retries < 10:
            response = client.get_burn(burn_uid)
            is_burning = response["data"]["status"] != 'done'
            time.sleep(15)
            retries += 1

        burn_response = client.get_burn(burn_uid)
        assert burn_response["success"] is True
        assert burn_response["data"]["status"] == 'done'

        final_asset_burned_status = False
        retries = 0

        while final_asset_burned_status is False and retries < 10:
            response = client.get_asset(asset_uid)
            final_asset_burned_status = response["data"]["is_burned"]
            time.sleep(15)
            retries += 1

        final_asset = client.get_asset(asset_uid)
        assert final_asset["success"] is True
        assert final_asset["data"]["is_burned"] is True
