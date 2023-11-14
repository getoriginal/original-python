import asyncio
import time
import random
import string
from typing import Any, Awaitable, Callable


def wait_for(condition: Callable[[], Any], timeout: int = 5):
    start = time.time()

    while True:
        if timeout < (time.time() - start):
            raise Exception("Timeout")

        try:
            if condition():
                break
        except Exception:
            pass

        time.sleep(1)


async def wait_for_async(
        condition: Callable[..., Awaitable[Any]], timeout: int = 5, **kwargs
):
    start = time.time()

    while True:
        if timeout < (time.time() - start):
            raise Exception("Timeout")

        try:
            if await condition(**kwargs):
                break
        except Exception:
            pass

        await asyncio.sleep(1)


def get_random_string(length: int):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for i in range(length))
    return random_string
