import time

import globals as gbl

from original_sdk import OriginalAsyncClient
from original_sdk.utils import get_random_string


class TestClientE2E:
    async def test_full_allocate_claim_flow(self, async_client: OriginalAsyncClient):
        allocation_data = {
            "amount": 0.001,
            "nonce": get_random_string(8),
            "reward_uid": gbl.env_data["test_app_reward_uid"],
            "to_user_uid": gbl.env_data["test_app_user_uid"],
        }
        response = await async_client.create_allocation(**allocation_data)
        allocation_uid = response["data"]["uid"]
        is_allocating = True
        retries = 0

        while is_allocating is True and retries < gbl.env_data["test_retry_counter"]:
            response = await async_client.get_allocation(allocation_uid)
            is_allocating = response["data"]["status"] != "done"
            if is_allocating:
                time.sleep(15)
            retries += 1

        allocation_response = await async_client.get_allocation(allocation_uid)
        assert (
            allocation_response["success"] is True
        ), f"Allocation {allocation_uid} is not done."

        claim_data = {
            "reward_uid": gbl.env_data["test_app_reward_uid"],
            "from_user_uid": gbl.env_data["test_app_user_uid"],
            "to_address": gbl.env_data["test_claim_to_address"],
        }

        response = await async_client.create_claim(**claim_data)
        claim_uid = response["data"]["uid"]
        is_claiming = True

        while is_claiming is True and retries < gbl.env_data["test_retry_counter"]:
            response = await async_client.get_claim(claim_uid)
            is_claiming = response["data"]["status"] != "done"
            if is_claiming:
                time.sleep(15)
            retries += 1

        claim_response = await async_client.get_claim(claim_uid)
        assert claim_response["success"] is True, f"Claim {claim_uid} is not done."
