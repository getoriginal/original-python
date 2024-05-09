import globals as gbl

from original_sdk import ClientError, OriginalClient


class TestClientE2E:

    def test_get_collection(self, client: OriginalClient):
        response = client.get_collection(gbl.env_data["test_app_collection_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_app_collection_uid"]

    def test_get_collection_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_collection("not_found")
        except ClientError as e:
            assert e.status == 404