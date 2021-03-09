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
