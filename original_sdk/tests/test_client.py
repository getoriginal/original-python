import os

import jwt
from dotenv import load_dotenv
from original_sdk import OriginalClient

load_dotenv()

TEST_API_KEY = os.getenv("TEST_API_KEY")
TEST_API_SECRET = os.getenv("TEST_API_SECRET")


class TestClient:
    def test_token(self, client: OriginalClient):
        token = client.token
        assert type(token) is str
        payload = jwt.decode(token, client.api_secret, algorithms=["HS256"])
        assert payload.get("api_key") == TEST_API_KEY

    def test_default_params(self, client: OriginalClient):
        assert client.get_default_params() == {
            "api_key": TEST_API_KEY,
            "api_secret": TEST_API_SECRET,
        }

    def test_default_base_url(self):
        client = OriginalClient(api_key=TEST_API_KEY, api_secret=TEST_API_SECRET)
        assert client.base_url == "https://api-sandbox.getoriginal.com/api/v1"

    def test_base_url_is_set(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            base_url="http://localhost:8000",
        )
        assert client.base_url == "http://localhost:8000"

    def test_base_url_removes_trailing_slashes(self):
        client = OriginalClient(
            api_key=TEST_API_KEY,
            api_secret=TEST_API_SECRET,
            base_url="http://localhost:8000/",
        )
        assert client.base_url == "http://localhost:8000"
