from typing import Any, Generator, Literal

from zhtools.type_hint import AnyCallable


class LazyLoadData:
    """
    Used for lazy loading of data, usually loading when data is used
    on the first time.
    """
    def __init__(self,
                 loader: AnyCallable,
                 *args,
                 **kwargs):
        self.loader = loader
        self.args = args
        self.kwargs = kwargs
        self._data = None

    @property
    def data(self) -> Any:
        if self._data is None:
            self._data = self.loader(*self.args, **self.kwargs)

        return self._data

    def refresh(self) -> Any:
        self._data = self.loader(*self.args, **self.kwargs)
        return self._data

    def __enter__(self):
        self.refresh()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.refresh()


def lazy_load(tp: Literal['dict', 'list']):

    def decorator(func):
        match tp:
            case 'dict':
                return LazyLoadDict(func)
            case 'list':
                return LazyLoadList(func)
            case _:
                return LazyLoadData(func)

    return decorator


class LazyLoadDict(LazyLoadData):

    def __getitem__(self, item: Any) -> Any:
        return self.data[item]

    def get(self, key: Any, default: Any = None) -> Any:
        return self.data.get(key, default)

    def keys(self) -> set:
        return self.data.keys()

    def values(self) -> set:
        return self.data.values()

    def items(self) -> Generator[tuple[Any, Any], None, None]:
        return self.data.items()

    def __iter__(self):
        return iter(self.data)


class LazyLoadList(LazyLoadData):

    def __getitem__(self, item: int) -> Any:
        return self.data[item]

    def __iter__(self):
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def append(self, val: Any):
        self.data.append(val)

    def __delitem__(self, key: int):
        del self.data[key]

