from typing import Union

from zhtools.code_generator.orms.generator import Column


class SqlalchemyColumn(Column):
    BASE_CLS = 'Base'
    TYPES = {
        'int': 'Integer',
        'bigint': 'Integer',
        'smallint': 'Integer',
        'tinyint': 'Integer',
        'varchar': 'String',
        'text': 'Text',
        'char': 'String',
        'datetime': 'DateTime',
        'date': 'Date'
    }

    def get_params(self) -> dict[str, Union[str, int, float, bool]]:
        kw = super().get_params()
        if self.primary_key:
            kw['primary_key'] = True
        return kw

    def render(self) -> str:
        kw = self.get_params()
        params = ', '.join([f"{k}='{v}'" if isinstance(v, str) else f'{k}={v}'
                            for k, v in kw.items()])
        type_col = self.get_type_col()
        type_params = str(self.type_param) if 'int' not in self.type else None
        if type_params and type_params != 'None':
            type_col = f'{type_col}({type_params})'
        p = [type_col, params]
        return f'{self.name} = Column({", ".join([i for i in p if i and i != "None"])})'
