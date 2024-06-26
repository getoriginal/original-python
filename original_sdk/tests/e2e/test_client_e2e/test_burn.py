import globals as gbl

from original_sdk import OriginalClient


class TestClientBurnE2E:
    def test_get_burn_by_user_uid(self, client: OriginalClient):
        response = client.get_burns_by_user_uid(gbl.env_data["test_app_user_uid"])
        assert isinstance(response["data"], list)
