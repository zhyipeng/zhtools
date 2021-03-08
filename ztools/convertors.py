def underline_to_camel_case(v: str) -> str:
    return v.replace('_', ' ').title().replace(' ', '')


def underline_to_small_camel_case(v: str) -> str:
    v = underline_to_camel_case(v)
    return v[0].lower() + v[1:]


def camel_case_to_underline(v: str) -> str:
    ret = v[0].lower()
    for i in v[1:]:
        if i.isupper():
            ret += '_'

        ret += i.lower()

    return ret
