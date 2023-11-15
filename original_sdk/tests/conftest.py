import asyncio
import os

import pytest

from original_sdk import OriginalClient
from original_sdk.async_client import OriginalAsyncClient


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail(f"previous test failed ({previousfailed.name})")


def pytest_configure(config):
    config.addinivalue_line("markers", "incremental: mark test incremental")


@pytest.fixture(scope="module")
def client():
    base_url = os.environ.get("TEST_ENDPOINT")
    options = {"base_url": base_url} if base_url else {}
    return OriginalClient(
        api_key=os.environ["TEST_API_KEY"],
        api_secret=os.environ["TEST_API_SECRET"],
        timeout=10,
        **options,
    )


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def async_client():
    base_url = os.environ.get("TEST_ORIGINAL_HOST")
    options = {"base_url": base_url} if base_url else {}
    async with OriginalAsyncClient(
        api_key=os.environ["TEST_API_KEY"],
        api_secret=os.environ["TEST_API_SECRET"],
        timeout=10,
        **options,
    ) as original_client:
        yield original_client
