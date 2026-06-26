"""等待辅助。"""

from __future__ import annotations

import time
from collections.abc import Callable


def wait_until(predicate: Callable[[], bool], timeout: float, interval: float = 0.5) -> bool:
    end_time = time.time() + timeout
    while time.time() < end_time:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()
