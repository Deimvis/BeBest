import time
import math


def calculate_rank(publish_timestamp: int) -> int:
    days_left = (int(time.time()) - publish_timestamp) // (24 * 60 * 60)
    return max(25 - days_left, 0)
