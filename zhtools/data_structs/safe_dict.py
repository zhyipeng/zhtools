from typing import Any


class NoKey:
    def __init__(self, k: Any) -> None:
        self.k = k

    def __str__(self) -> str:
        return f'key {self.k} not exists'

    def __bool__(self) -> bool:
        return False

    def __getitem__(self, item: Any) -> Any:
        return NoKey(f'{self.k}.{item}')


class SafeDict(dict):
    def __getitem__(self, key: Any) -> Any:
        if key not in self:
            return NoKey(key)
        return super().__getitem__(key)
