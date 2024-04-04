import os
import time

import pytest
from dotenv import load_dotenv

from original_sdk import ClientError, OriginalClient
from original_sdk.utils import get_random_string

load_dotenv()

TEST_APP_USER_EMAIL = os.getenv("TEST_APP_USER_EMAIL")
TEST_APP_USER_UID = os.getenv("TEST_APP_USER_UID")
TEST_APP_USER_CLIENT_ID = os.getenv("TEST_APP_USER_CLIENT_ID")
TEST_APP_COLLECTION_UID = os.getenv("TEST_APP_COLLECTION_UID")
TEST_ASSET_UID = os.getenv("TEST_ASSET_UID")
TEST_TRANSFER_TO_WALLET_ADDRESS = os.getenv("TEST_TRANSFER_TO_WALLET_ADDRESS")
TEST_TRANSFER_TO_USER_UID = os.getenv("TEST_TRANSFER_TO_USER_UID")
TEST_APP_REWARD_UID = os.getenv("TEST_APP_REWARD_UID")
TEST_ALLOCATION_UID = os.getenv("TEST_ALLOCATION_UID")
TEST_CLAIM_UID = os.getenv("TEST_CLAIM_UID")
TEST_CLAIM_TO_ADDRESS = os.getenv("TEST_CLAIM_TO_ADDRESS")
TEST_ACCEPTANCE_CHAIN_ID = os.getenv("TEST_ACCEPTANCE_CHAIN_ID")
TEST_ACCEPTANCE_NETWORK = os.getenv("TEST_ACCEPTANCE_NETWORK")
TEST_RETRY_COUNTER = 30


class TestClientE2E:
    def test_create_user_with_params(self, client: OriginalClient):
        user_external_id = get_random_string(8)
        response = client.create_user(
            email=f"{user_external_id}@test.com", user_external_id=user_external_id
        )
        assert response["data"]["uid"] is not None

    def test_create_user_with_deprecated_client_id(self, client: OriginalClient):
        client_id = get_random_string(8)
        response = client.create_user(
            email=f"{client_id}@test.com", client_id=client_id
        )
        assert response["data"]["uid"] is not None

    def test_create_user_with_no_params(self, client: OriginalClient):
        response = client.create_user()
        assert response["data"]["uid"] is not None

    def test_error_message(self, client: OriginalClient):
        client_id = "existing_user"
        with pytest.raises(
            ClientError,
            match="'message': 'User already exists.'}",
        ):
            client.create_user(email=f"{client_id}@test.com", client_id=client_id)

    def test_get_user(self, client: OriginalClient):
        response = client.get_user(TEST_APP_USER_UID)
        assert response["data"]["uid"] == TEST_APP_USER_UID
        assert response["data"]["email"] == TEST_APP_USER_EMAIL

    def test_get_user_by_email(self, client: OriginalClient):
        response = client.get_user_by_email(TEST_APP_USER_EMAIL)
        assert response["data"]["uid"] == TEST_APP_USER_UID
        assert response["data"]["email"] == TEST_APP_USER_EMAIL

    def test_get_user_by_user_external_id(self, client: OriginalClient):
        response = client.get_user_by_user_external_id(TEST_APP_USER_CLIENT_ID)
        assert response["data"]["uid"] == TEST_APP_USER_UID
        assert response["data"]["email"] == TEST_APP_USER_EMAIL

    def test_get_user_by_client_id(self, client: OriginalClient):
        response = client.get_user_by_client_id(TEST_APP_USER_CLIENT_ID)
        assert response["data"]["uid"] == TEST_APP_USER_UID
        assert response["data"]["email"] == TEST_APP_USER_EMAIL

    def test_get_user_by_client_id_with_no_results(self, client: OriginalClient):
        response = client.get_user_by_client_id("no_results")
        assert response["data"] is None

    def test_get_user_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_user("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_get_collection(self, client: OriginalClient):
        response = client.get_collection(TEST_APP_COLLECTION_UID)
        assert response["data"]["uid"] == TEST_APP_COLLECTION_UID

    def test_get_collection_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_collection("not_found")
        except ClientError as e:
            assert e.status == 404

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
            "user_uid": TEST_APP_USER_UID,
            "asset_external_id": asset_name,
            "collection_uid": TEST_APP_COLLECTION_UID,
        }
        response = client.create_asset(**request_data)
        assert response["data"]["uid"] is not None

    def test_create_asset_with_deprecated_client_id(self, client: OriginalClient):
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

    def test_create_asset_with_no_client_id(self, client: OriginalClient):
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
            "collection_uid": TEST_APP_COLLECTION_UID,
        }
        response = client.create_asset(**request_data)
        assert response["data"]["uid"] is not None

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
            "user_uid": TEST_APP_USER_UID,
            "client_id": asset_name,
            "collection_uid": TEST_APP_COLLECTION_UID,
        }
        asset_response = client.create_asset(**request_data)
        asset_uid = asset_response["data"]["uid"]
        is_transferable = False
        retries = 0

        while is_transferable is False and retries < TEST_RETRY_COUNTER:
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

    def test_get_asset(self, client: OriginalClient):
        response = client.get_asset(TEST_ASSET_UID)
        assert response["data"]["uid"] == TEST_ASSET_UID

    def test_get_asset_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_asset("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_get_asset_by_user_uid(self, client: OriginalClient):
        response = client.get_assets_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_get_asset_by_user_uid_with_no_results(self, client: OriginalClient):
        response = client.get_assets_by_user_uid("no_results")
        assert response["data"] == []

    def test_get_transfer_by_user_uid(self, client: OriginalClient):
        response = client.get_transfers_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_get_burn_by_user_uid(self, client: OriginalClient):
        response = client.get_burns_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_get_deposit(self, client: OriginalClient):
        response = client.get_deposit(TEST_TRANSFER_TO_USER_UID)
        assert response["data"]["wallet_address"] == TEST_TRANSFER_TO_WALLET_ADDRESS
        assert response["data"]["chain_id"] == int(TEST_ACCEPTANCE_CHAIN_ID)
        assert response["data"]["network"] == TEST_ACCEPTANCE_NETWORK

    def test_get_reward(self, client: OriginalClient):
        response = client.get_reward(TEST_APP_REWARD_UID)
        assert response["data"]["uid"] == TEST_APP_REWARD_UID

    def test_get_reward_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_reward("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_create_allocation(self, client: OriginalClient):
        allocation_data = {
            "amount": 0.001,
            "nonce": get_random_string(8),
            "reward_uid": TEST_APP_REWARD_UID,
            "to_user_uid": TEST_APP_USER_UID,
        }
        response = client.create_allocation(**allocation_data)
        assert response["data"]["uid"] is not None

    def test_get_allocation(self, client: OriginalClient):
        response = client.get_allocation(TEST_ALLOCATION_UID)
        assert response["data"]["uid"] == TEST_ALLOCATION_UID

    def test_get_allocation_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_allocation("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_get_allocations_by_user_uid(self, client: OriginalClient):
        response = client.get_allocations_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_get_allocations_by_user_uid_with_no_results(self, client: OriginalClient):
        response = client.get_allocations_by_user_uid("no_results")
        assert response["data"] == []

    def test_create_claim(self, client: OriginalClient):
        claim_data = {
            "reward_uid": TEST_APP_REWARD_UID,
            "from_user_uid": TEST_APP_USER_UID,
            "to_address": TEST_CLAIM_TO_ADDRESS,
        }
        response = client.create_claim(**claim_data)
        assert response["data"]["uid"] is not None

    def test_get_claim(self, client: OriginalClient):
        response = client.get_claim(TEST_CLAIM_UID)
        assert response["data"]["uid"] == TEST_CLAIM_UID

    def test_get_claim_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_claim("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_get_claims_by_user_uid(self, client: OriginalClient):
        response = client.get_claims_by_user_uid(TEST_APP_USER_UID)
        assert isinstance(response["data"], list)

    def test_get_claims_by_user_uid_with_no_results(self, client: OriginalClient):
        response = client.get_claims_by_user_uid("no_results")
        assert response["data"] == []

    def test_full_create_transfer_burn_asset_flow(self, client: OriginalClient):
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

        while is_transferable is False and retries < TEST_RETRY_COUNTER:
            response = client.get_asset(asset_uid)
            is_transferable = response["data"]["is_transferable"]
            if not is_transferable:
                time.sleep(15)
            retries += 1

        assert is_transferable, f"Asset {asset_uid} is not transferable."

        transfer_response = client.create_transfer(
            asset_uid=asset_uid,
            from_user_uid=TEST_APP_USER_UID,
            to_address=TEST_TRANSFER_TO_WALLET_ADDRESS,
        )
        assert transfer_response["success"] is True
        transfer_uid = transfer_response["data"]["uid"]
        is_transferring = True
        retries = 0

        while is_transferring is True and retries < TEST_RETRY_COUNTER:
            response = client.get_asset(asset_uid)
            is_transferring = response["data"]["is_transferring"]
            if is_transferring:
                time.sleep(15)
            retries += 1

        transfer_response = client.get_transfer(transfer_uid)
        assert (
            transfer_response["success"] is True
        ), f"Transfer {transfer_uid} is not done."
        assert transfer_response["data"]["status"] == "done"

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

        while is_burning is True and retries < TEST_RETRY_COUNTER:
            response = client.get_burn(burn_uid)
            is_burning = response["data"]["status"] != "done"
            if is_burning:
                time.sleep(15)
            retries += 1

        burn_response = client.get_burn(burn_uid)
        assert burn_response["success"] is True, f"Burn {burn_uid} is not done."
        assert burn_response["data"]["status"] == "done"

        final_asset_burned_status = False
        retries = 0

        while final_asset_burned_status is False and retries < TEST_RETRY_COUNTER:
            response = client.get_asset(asset_uid)
            final_asset_burned_status = response["data"]["is_burned"]
            if not final_asset_burned_status:
                time.sleep(15)
            retries += 1

        final_asset = client.get_asset(asset_uid)
        assert final_asset["success"] is True, f"Asset {asset_uid} is not burned."
        assert final_asset["data"]["is_burned"] is True

    def test_full_allocate_claim_flow(self, client: OriginalClient):
        allocation_data = {
            "amount": 0.001,
            "nonce": get_random_string(8),
            "reward_uid": TEST_APP_REWARD_UID,
            "to_user_uid": TEST_APP_USER_UID,
        }
        response = client.create_allocation(**allocation_data)
        allocation_uid = response["data"]["uid"]
        is_allocating = True
        retries = 0

        while is_allocating is True and retries < TEST_RETRY_COUNTER:
            response = client.get_allocation(allocation_uid)
            is_allocating = response["data"]["status"] != "done"
            if is_allocating:
                time.sleep(15)
            retries += 1

        allocation_response = client.get_allocation(allocation_uid)
        assert (
            allocation_response["success"] is True
        ), f"Allocation {allocation_uid} is not done."

        claim_data = {
            "reward_uid": TEST_APP_REWARD_UID,
            "from_user_uid": TEST_APP_USER_UID,
            "to_address": TEST_CLAIM_TO_ADDRESS,
        }

        response = client.create_claim(**claim_data)
        claim_uid = response["data"]["uid"]
        is_claiming = True

        while is_claiming is True and retries < TEST_RETRY_COUNTER:
            response = client.get_claim(claim_uid)
            is_claiming = response["data"]["status"] != "done"
            if is_claiming:
                time.sleep(15)
            retries += 1

        claim_response = client.get_claim(claim_uid)
        assert claim_response["success"] is True, f"Claim {claim_uid} is not done."
