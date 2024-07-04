from zhtools.typing import AnyNumber


def safe_divide[T: AnyNumber](
    a: T,
    b: T,
    decimal_len: int = 2,
    while_zero: T = 0,
) -> str:
    """
    Safe division avoiding ZeroDivisionError
    :param a: dividend
    :param b: divisor
    :param decimal_len: decimal digits
    :param while_zero:
    :return: division result
    """
    fm = f"%.{decimal_len}f"
    return fm % (a / b) if b else fm % while_zero  # type: ignore
