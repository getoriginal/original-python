import asyncio
import os

import globals as gbl
import pytest

from original_sdk import OriginalClient
from original_sdk.async_client import OriginalAsyncClient


@pytest.fixture(autouse=True)
def populate_globals():
    test_app_user_email = os.getenv("TEST_APP_USER_EMAIL")
    test_app_user_uid = os.getenv("TEST_APP_USER_UID")
    test_app_user_client_id = os.getenv("TEST_APP_USER_CLIENT_ID")
    test_app_collection_uid = os.getenv("TEST_APP_COLLECTION_UID")
    test_asset_uid = os.getenv("TEST_ASSET_UID")
    test_transfer_to_wallet_address = os.getenv("TEST_TRANSFER_TO_WALLET_ADDRESS")
    test_transfer_to_user_uid = os.getenv("TEST_TRANSFER_TO_USER_UID")
    test_app_reward_uid = os.getenv("TEST_APP_REWARD_UID")
    test_allocation_uid = os.getenv("TEST_ALLOCATION_UID")
    test_claim_uid = os.getenv("TEST_CLAIM_UID")
    test_claim_to_address = os.getenv("TEST_CLAIM_TO_ADDRESS")
    test_acceptance_chain_id = int(os.getenv("TEST_ACCEPTANCE_CHAIN_ID"))
    test_acceptance_network = os.getenv("TEST_ACCEPTANCE_NETWORK")
    test_multi_chain_collection_uid = os.getenv("TEST_MULTI_CHAIN_COLLECTION_UID")
    test_multi_chain_transfer_to_user_wallet = os.getenv(
        "TEST_MULTI_CHAIN_TRANSFER_TO_USER_WALLET"
    )
    test_multi_chain_transfer_to_user_uid = os.getenv(
        "TEST_MULTI_CHAIN_TRANSFER_TO_USER_UID"
    )
    test_retry_counter = 30

    gbl.env_data = {
        "test_app_user_email": test_app_user_email,
        "test_app_user_uid": test_app_user_uid,
        "test_app_user_client_id": test_app_user_client_id,
        "test_app_collection_uid": test_app_collection_uid,
        "test_asset_uid": test_asset_uid,
        "test_transfer_to_wallet_address": test_transfer_to_wallet_address,
        "test_transfer_to_user_uid": test_transfer_to_user_uid,
        "test_app_reward_uid": test_app_reward_uid,
        "test_allocation_uid": test_allocation_uid,
        "test_claim_uid": test_claim_uid,
        "test_claim_to_address": test_claim_to_address,
        "test_acceptance_chain_id": test_acceptance_chain_id,
        "test_acceptance_network": test_acceptance_network,
        "test_retry_counter": test_retry_counter,
        "test_multi_chain_collection_uid": test_multi_chain_collection_uid,
        "test_multi_chain_transfer_to_user_wallet": test_multi_chain_transfer_to_user_wallet,
        "test_multi_chain_transfer_to_user_uid": test_multi_chain_transfer_to_user_uid,
    }


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
    base_url = os.environ.get("TEST_ORIGINAL_HOST")
    api_version = os.environ.get("TEST_ORIGINAL_API_VERSION")
    options = {"base_url": base_url} if base_url else {}
    options = {**options, "api_version": api_version} if api_version else {**options}
    return OriginalClient(
        api_key=os.environ["TEST_API_KEY"],
        api_secret=os.environ["TEST_API_SECRET"],
        timeout=10,
        **options,
    )


@pytest.fixture(scope="module")
def multi_chain_client():
    base_url = os.environ.get("TEST_ORIGINAL_HOST")
    api_version = os.environ.get("TEST_ORIGINAL_API_VERSION")
    options = {"base_url": base_url} if base_url else {}
    options = {**options, "api_version": api_version} if api_version else {**options}
    return OriginalClient(
        api_key=os.environ["TEST_MULTI_CHAIN_API_KEY"],
        api_secret=os.environ["TEST_MULTI_CHAIN_API_SECRET"],
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
    api_version = os.environ.get("TEST_ORIGINAL_API_VERSION")
    options = {"base_url": base_url} if base_url else {}
    options = {**options, "api_version": api_version} if api_version else {**options}
    async with OriginalAsyncClient(
        api_key=os.environ["TEST_API_KEY"],
        api_secret=os.environ["TEST_API_SECRET"],
        timeout=10,
        **options,
    ) as original_client:
        yield original_client


@pytest.fixture(scope="module")
async def async_multi_chain_client():
    base_url = os.environ.get("TEST_ORIGINAL_HOST")
    api_version = os.environ.get("TEST_ORIGINAL_API_VERSION")
    options = {"base_url": base_url} if base_url else {}
    options = {**options, "api_version": api_version} if api_version else {**options}
    async with OriginalAsyncClient(
        api_key=os.environ["TEST_MULTI_CHAIN_API_KEY"],
        api_secret=os.environ["TEST_MULTI_CHAIN_API_SECRET"],
        timeout=10,
        **options,
    ) as original_client:
        yield original_client
