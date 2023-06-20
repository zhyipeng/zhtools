from collections import defaultdict
from typing import TypeVar


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


def camel_case_data_to_underline(data: dict | list) -> dict | list:
    if isinstance(data, list):
        return [camel_case_data_to_underline(it) for it in data]
    elif isinstance(data, dict):
        ret = {}
        for k, v in data.items():
            new_k = camel_case_to_underline(k)
            if isinstance(v, (list, dict)):
                v = camel_case_data_to_underline(v)
            ret[new_k] = v

        return ret
    return data


def underline_case_data_to_camel(data: dict | list) -> dict | list:
    if isinstance(data, list):
        return [underline_case_data_to_camel(it) for it in data]
    elif isinstance(data, dict):
        ret = {}
        for k, v in data.items():
            new_k = underline_to_small_camel_case(k)
            if isinstance(v, (list, dict)):
                v = underline_case_data_to_camel(v)
            ret[new_k] = v

        return ret
    return data


def deconstruct_defaultdict(d: defaultdict | dict) -> dict:
    """Recursively convert defaultdict to dict"""
    if isinstance(d, defaultdict):
        d = dict(d)

    for k in d:
        if isinstance(d[k], defaultdict):
            d[k] = deconstruct_defaultdict(d[k])
    return d


K = TypeVar('K')
V = TypeVar('V')


def transpose_dict(data: dict[K, V]) -> dict[V, set[K]]:
    ret = defaultdict(set)
    for k, v in data.items():
        ret[v].add(k)
    return dict(ret)


T = TypeVar('T')


def group_by_key(data: list[T], key: str) -> dict[str, list[T]]:
    ret = defaultdict(list)
    for item in data:
        if isinstance(item, dict):
            k = item[key]
        else:
            k = getattr(item, key)
        ret[k].append(item)

    return dict(ret)
