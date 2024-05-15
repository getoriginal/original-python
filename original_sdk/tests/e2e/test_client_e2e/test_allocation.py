import globals as gbl

from original_sdk import ClientError, OriginalClient
from original_sdk.utils import get_random_string


class TestClientAllocationE2E:
    def test_create_allocation(self, client: OriginalClient):
        allocation_data = {
            "amount": 0.001,
            "nonce": get_random_string(8),
            "reward_uid": gbl.env_data["test_app_reward_uid"],
            "to_user_uid": gbl.env_data["test_app_user_uid"],
        }
        response = client.create_allocation(**allocation_data)
        assert response["data"]["uid"] is not None

    def test_get_allocation(self, client: OriginalClient):
        response = client.get_allocation(gbl.env_data["test_allocation_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_allocation_uid"]

    def test_get_allocation_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_allocation("not_found")
        except ClientError as e:
            assert e.status == 404

    def test_get_allocations_by_user_uid(self, client: OriginalClient):
        response = client.get_allocations_by_user_uid(gbl.env_data["test_app_user_uid"])
        assert isinstance(response["data"], list)

    def test_get_allocations_by_user_uid_with_no_results(self, client: OriginalClient):
        response = client.get_allocations_by_user_uid("no_results")
        assert response["data"] == []
