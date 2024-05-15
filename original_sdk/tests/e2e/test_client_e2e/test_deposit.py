import globals as gbl

from original_sdk import OriginalClient


class TestClientDepositE2E:
    def test_get_deposit(self, client: OriginalClient):
        response = client.get_deposit(gbl.env_data["test_transfer_to_user_uid"])
        assert (
            response["data"]["wallet_address"]
            == gbl.env_data["test_transfer_to_wallet_address"]
        )
        assert response["data"]["chain_id"] == gbl.env_data["test_acceptance_chain_id"]
        assert response["data"]["network"] == gbl.env_data["test_acceptance_network"]
