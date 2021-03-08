import uuid


def uuid4_hex(duplicate: int = 1) -> str:
    """
    :param duplicate: duplicate times
    :return: uuid string
    """
    s = ''
    for _ in range(duplicate):
        s += uuid.uuid4().hex
    return s
