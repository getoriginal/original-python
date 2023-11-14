import os
import time
import jwt
import pytest
from dotenv import load_dotenv

from original import Original

load_dotenv()

TEST_API_KEY = os.getenv('TEST_API_KEY')
TEST_API_SECRET = os.getenv('TEST_API_SECRET')


class TestClient:

    def test_token(self, client: Original):
        token = client.token
        assert type(token) is str
        payload = jwt.decode(token, client.api_secret, algorithms=["HS256"])
        assert payload.get("api_key") == TEST_API_KEY

    def test_default_params(self, client: Original):
        assert client.get_default_params() == {"api_key": TEST_API_KEY, "api_secret": TEST_API_SECRET}
