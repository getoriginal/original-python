import globals as gbl

from original_sdk import OriginalAsyncClient


class TestAsyncClientDepositE2E:
    async def test_get_deposit(self, async_client: OriginalAsyncClient):
        response = await async_client.get_deposit(
            gbl.env_data["test_transfer_to_user_uid"]
        )
        assert (
            response["data"]["wallet_address"]
            == gbl.env_data["test_transfer_to_wallet_address"]
        )
        assert response["data"]["chain_id"] == gbl.env_data["test_acceptance_chain_id"]
        assert response["data"]["network"] == gbl.env_data["test_acceptance_network"]

    async def test_get_deposit_multi_chain(self, async_multi_chain_client: OriginalAsyncClient):
        response = await async_multi_chain_client.get_deposit(
            gbl.env_data["test_multi_chain_transfer_to_user_uid"],
            gbl.env_data["test_multi_chain_collection_uid"],
        )
        assert (
            response["data"]["wallet_address"]
            == gbl.env_data["test_multi_chain_transfer_to_user_wallet"]
        )
        assert response["data"]["chain_id"] == gbl.env_data["test_acceptance_chain_id"]
        assert response["data"]["network"] == gbl.env_data["test_acceptance_network"]
