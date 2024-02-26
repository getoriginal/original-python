from datetime import datetime, timezone

from original_sdk.types.original_response import OriginalResponse
from original_sdk.types.rate_limit import RateLimitInfo


def test_original_response_initialization_without_rate_limit():
    response_data = {"data": "test_data"}
    headers = {"content-type": "application/json"}
    status_code = 200

    resp = OriginalResponse(response_data, headers, status_code)

    assert resp["data"] == "test_data"
    assert resp.headers() == headers
    assert resp.status_code() == status_code
    assert resp.rate_limit() is None


def test_original_response_initialization_with_rate_limit():
    response_data = {"data": "test_data"}
    headers = {
        "content-type": "application/json",
        "x-ratelimit-limit": "100",
        "x-ratelimit-remaining": "99",
        "x-ratelimit-reset": str(datetime.now(timezone.utc).timestamp()),
    }
    status_code = 200

    resp = OriginalResponse(response_data, headers, status_code)

    rate_limit = resp.rate_limit()
    assert rate_limit is not None
    assert rate_limit.limit == 100
    assert rate_limit.remaining == 99
    assert isinstance(rate_limit.reset, datetime)
    assert rate_limit.reset.tzinfo is timezone.utc


def test_original_response_with_malformed_rate_limit_headers():
    response_data = {"data": "test_data"}
    headers = {
        "content-type": "application/json",
        "x-ratelimit-limit": "malformed",
        "x-ratelimit-remaining": "malformed",
        "x-ratelimit-reset": "malformed",
    }
    status_code = 200

    resp = OriginalResponse(response_data, headers, status_code)

    assert isinstance(resp.rate_limit(), RateLimitInfo)


def test_original_response_headers_and_status_code_accessors():
    response_data = {"data": "test_data"}
    headers = {"content-type": "application/json;charset=utf-8"}
    status_code = 404

    resp = OriginalResponse(response_data, headers, status_code)

    assert resp.headers() == headers
    assert resp.status_code() == status_code
