"""
随机延迟模块
用于模拟人类行为，降低被风控的概率
"""

import random
from time import sleep


def random_delay(min_sec: float, max_sec: float) -> float:
    """
    生成随机延迟

    Args:
        min_sec: 最小延迟（秒）
        max_sec: 最大延迟（秒）

    Returns:
        实际延迟时间
    """
    delay = random.uniform(min_sec, max_sec)
    sleep(delay)
    return delay


def page_delay() -> float:
    """页面间延迟（5-10秒）"""
    return random_delay(5, 10)


def job_delay() -> float:
    """职位间延迟（2-4秒）"""
    return random_delay(2, 4)


def click_delay() -> float:
    """点击后延迟（1-2秒）"""
    return random_delay(1, 2)


def scroll_delay() -> float:
    """滚动后延迟（0.5-1.5秒）"""
    return random_delay(0.5, 1.5)
