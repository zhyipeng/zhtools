from typing import Union

from .generator import Column


class TortoiseColumn(Column):
    TYPES: dict[str, str] = {
        'int': 'IntField',
        'bigint': 'IntField',
        'smallint': 'IntField',
        'tinyint': 'IntField',
        'varchar': 'CharField',
        'text': 'TextField',
        'longtext': 'TextField',
        'char': 'CharField',
        'datetime': 'DatetimeField',
        'date': 'DateField',
    }

    def get_type_col(self) -> str:
        return 'fields.' + self.TYPES[self.type]

    def get_params(self) -> dict[str, Union[str, int, float, bool]]:
        kw = self.kwargs.copy()
        default = self.default
        if default is not None:
            if default == 'null':
                kw['null'] = True
            else:
                if 'int' in self.type:
                    kw['default'] = int(default)
                else:
                    kw['default'] = default

        if self.nullable:
            kw['null'] = True

        if self.primary_key:
            kw['pk'] = True

        return kw
