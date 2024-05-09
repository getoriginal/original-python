import globals as gbl
import pytest

from original_sdk import ClientError, OriginalClient
from original_sdk.utils import get_random_string


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
        response = client.get_user(gbl.env_data["test_app_user_uid"])
        assert response["data"]["uid"] == gbl.env_data["test_app_user_uid"]
        assert response["data"]["email"] == gbl.env_data["test_app_user_email"]

    def test_get_user_by_email(self, client: OriginalClient):
        response = client.get_user_by_email(gbl.env_data["test_app_user_email"])
        assert response["data"]["uid"] == gbl.env_data["test_app_user_uid"]
        assert response["data"]["email"] == gbl.env_data["test_app_user_email"]

    def test_get_user_by_user_external_id(self, client: OriginalClient):
        response = client.get_user_by_user_external_id(
            gbl.env_data["test_app_user_client_id"]
        )
        assert response["data"]["uid"] == gbl.env_data["test_app_user_uid"]
        assert response["data"]["email"] == gbl.env_data["test_app_user_email"]

    def test_get_user_by_client_id(self, client: OriginalClient):
        response = client.get_user_by_client_id(gbl.env_data["test_app_user_client_id"])
        assert response["data"]["uid"] == gbl.env_data["test_app_user_uid"]
        assert response["data"]["email"] == gbl.env_data["test_app_user_email"]

    def test_get_user_by_client_id_with_no_results(self, client: OriginalClient):
        response = client.get_user_by_client_id("no_results")
        assert response["data"] is None

    def test_get_user_not_found_throws_404(self, client: OriginalClient):
        try:
            client.get_user("not_found")
        except ClientError as e:
            assert e.status == 404
