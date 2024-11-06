import globals as gbl

from original_sdk import OriginalClient


class TestClientDepositE2E:
    def test_get_deposit(self, client: OriginalClient):
        user_uid = gbl.env_data["test_transfer_to_user_uid"]
        collection_uid = gbl.env_data["test_app_collection_uid"]
        response = client.get_deposit(user_uid, collection_uid)
        assert (
            response["data"]["wallet_address"]
            == gbl.env_data["test_transfer_to_wallet_address"]
        )
        assert response["data"]["chain_id"] == 80002
        assert response["data"]["network"] == "Amoy"
