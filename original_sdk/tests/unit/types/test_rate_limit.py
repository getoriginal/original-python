from datetime import datetime, timezone

import pytest

from original_sdk.types.rate_limit import RateLimitInfo


def test_rate_limit_info_initialization():
    limit = 100
    remaining = 99
    reset_time = datetime.now(timezone.utc)

    rate_limit_info = RateLimitInfo(limit=limit, remaining=remaining, reset=reset_time)

    assert rate_limit_info.limit == limit
    assert rate_limit_info.remaining == remaining
    assert rate_limit_info.reset == reset_time


def test_rate_limit_info_immutable():
    rate_limit_info = RateLimitInfo(
        limit=100, remaining=99, reset=datetime.now(timezone.utc)
    )

    # Check for the absence of setter methods indirectly validating immutability
    with pytest.raises(AttributeError):
        setattr(rate_limit_info, "limit", 50)
    with pytest.raises(AttributeError):
        setattr(rate_limit_info, "remaining", 48)
    with pytest.raises(AttributeError):
        setattr(rate_limit_info, "reset", datetime.now(timezone.utc))
