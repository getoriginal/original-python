import globals as gbl

from original_sdk import ClientError, OriginalAsyncClient
from original_sdk.utils import get_random_string


class TestAsyncClientAllocationE2E:
    async def test_create_allocation(self, async_client: OriginalAsyncClient):
        allocation_data = {
            "amount": 0.001,
            "nonce": get_random_string(8),
            "reward_uid": gbl.env_data["test_app_reward_uid"],
            "to_user_uid": gbl.env_data["test_app_user_uid"],
        }
        response = await async_client.create_allocation(**allocation_data)
        assert response["data"]["uid"] is not None

    async def test_get_allocation(self, async_client: OriginalAsyncClient):
        response = await async_client.get_allocation(
            gbl.env_data["test_allocation_uid"]
        )
        assert response["data"]["uid"] == gbl.env_data["test_allocation_uid"]

    async def test_get_allocation_not_found_throws_404(
        self, async_client: OriginalAsyncClient
    ):
        try:
            await async_client.get_allocation("not_found")
        except ClientError as e:
            assert e.status == 404

    async def test_get_allocations_by_user_uid(self, async_client: OriginalAsyncClient):
        response = await async_client.get_allocations_by_user_uid(
            gbl.env_data["test_app_user_uid"]
        )
        assert isinstance(response["data"], list)

    async def test_get_allocations_by_user_uid_with_no_results(
        self, async_client: OriginalAsyncClient
    ):
        response = await async_client.get_allocations_by_user_uid("no_results")
        assert response["data"] == []
