import random
import string
import uuid


def uuid4_hex(duplicate: int = 1) -> str:
    """
    Generate a uuid
    :param duplicate: duplicate times
    :return: uuid string
    """
    s = ''
    for _ in range(duplicate):
        s += uuid.uuid4().hex
    return s


def short_uuid() -> str:
    """
    Generate a short uuid
    :return:
    """
    uuid_ = uuid4_hex()
    chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
    s = ''
    for i in range(0, 8):
        sub = uuid_[i * 4:i * 4 + 4]
        x = int(sub, 16)
        s += chars[x % 0x3E]
    return s


def roll(min_: int = 0, max_: int = 1000000) -> int:
    return random.randint(min_, max_)


def roll_weight(weight: list[int]) -> int:
    """
    :param weight: [100, 200, 300]
    :return: 0/1/2
    """
    p = roll(0, weight[-1])
    for i, w in enumerate(weight):
        if p < w:
            return i
    return len(weight) - 1


def roll_rate(rate: int | float, max_: int = 10000) -> bool:
    return roll(0, max_) < rate
