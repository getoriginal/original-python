import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ContentTypeError

from original_sdk import ClientError
from original_sdk.async_client import OriginalAsyncClient


@pytest.fixture
async def async_client():
    client = OriginalAsyncClient(
        api_key="test_api_key",
        api_secret="test_api_secret",
        base_url="https://api-dev.getoriginal.com",
        api_version="v1",
        timeout=10,
    )
    await client.__aenter__()
    yield client
    await client.__aexit__(None, None, None)


@pytest.mark.asyncio
async def test_get_response_details_json(async_client):
    with patch("aiohttp.ClientResponse.json", new_callable=AsyncMock), patch(
        "aiohttp.ClientResponse.text", new_callable=AsyncMock
    ):
        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={"data": "test"})
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.status = 200

        json_response, headers, status = await async_client._get_response_details(
            mock_response
        )

        assert json_response == {"data": "test"}
        assert headers == {"Content-Type": "application/json"}
        assert status == 200


@pytest.mark.asyncio
async def test_get_response_details_non_json(async_client):
    mock_response = MagicMock()
    mock_response.headers = {"Content-Type": "text/plain"}
    mock_response.status = 400
    mock_response.json = MagicMock(
        side_effect=ContentTypeError(
            request_info=None,
            history=None,
            message="Attempt to decode JSON with unexpected mimetype: text/plain",
        )
    )
    mock_response.text = MagicMock(return_value=asyncio.Future())
    mock_response.text.return_value.set_result("Bad Request")

    with pytest.raises(ClientError) as exc_info:
        await async_client._get_response_details(mock_response)

    assert "Bad Request" in str(exc_info.value)
    assert exc_info.value.status == 400
    assert "Bad Request" in exc_info.value.message


@pytest.mark.asyncio
async def test_async_client_get_user(async_client):
    with patch("aiohttp.ClientSession.get", new_callable=MagicMock) as mock_get:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"data": "mocked_data"})

        mock_get.__name__ = "get"
        mock_get.return_value.__aenter__.return_value = mock_response

        response = await async_client.get_user("user_id")

        assert response["data"] == "mocked_data"
        mock_get.assert_called_once()


@pytest.mark.asyncio
async def test_async_client_create_user(async_client):
    with patch("aiohttp.ClientSession.post", new_callable=MagicMock) as mock_post:
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.json = AsyncMock(return_value={"data": "user_created"})
        mock_post.__name__ = "post"
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await async_client.create_user(
            email="test@example.com", user_external_id="client123"
        )

        assert response["data"] == "user_created"
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_async_client_edit_asset(async_client):
    with patch("aiohttp.ClientSession.put", new_callable=MagicMock) as mock_put:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"data": "asset_updated"})
        mock_put.__name__ = "put"
        mock_put.return_value.__aenter__.return_value = mock_response

        response = await async_client.edit_asset("asset_id", name="New Name")

        assert response["data"] == "asset_updated"
        mock_put.assert_called_once()


@pytest.mark.asyncio
async def test_async_client_delete_user(async_client):
    with patch("aiohttp.ClientSession.delete", new_callable=MagicMock) as mock_delete:
        mock_response = MagicMock()
        mock_response.status = 204  # No content
        mock_response.json = AsyncMock(return_value={"data": None})
        mock_delete.__name__ = "delete"
        mock_delete.return_value.__aenter__.return_value = mock_response

        response = await async_client.delete("user/user_id")

        assert response["data"] is None
        mock_delete.assert_called_once()


@pytest.mark.asyncio
async def test_async_client_patch_user_info(async_client):
    with patch("aiohttp.ClientSession.patch", new_callable=MagicMock) as mock_patch:
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"data": "user_info_updated"})
        mock_patch.__name__ = "patch"
        mock_patch.return_value.__aenter__.return_value = mock_response

        response = await async_client.patch("user/user_id", data={"name": "New Name"})

        assert response["data"] == "user_info_updated"
        mock_patch.assert_called_once()
