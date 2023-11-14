import os

import pytest

from original import Original


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
    return Original(
        api_key=os.environ["TEST_API_KEY"],
        api_secret=os.environ["TEST_API_SECRET"],
        timeout=10,
        **options,
    )


