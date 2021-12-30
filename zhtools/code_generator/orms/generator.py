import re
import traceback
from typing import Any, List, Tuple, Type, Union

from zhtools.data_structs.convertors import underline_to_camel_case

TYPES = {
    'int': 'IntCol',
    'bigint': 'IntCol',
    'smallint': 'ShortCol',
    'varchar': 'StrCol',
    'text': 'TextCol',
    'char': 'StrCol',
    'datetime': 'DatetimeCol',
    'date': 'DateCol',
    'tinyint': 'BoolCol',
}

KEYS = {'key', 'primary key', 'unique'}


class Column:
    BASE_CLS = 'Model'
    TYPES: dict[str, str] = {}

    def __init__(self,
                 name: str,
                 type: str,
                 type_param: Any = None,
                 nullable: bool = True,
                 default: Any = None,
                 primary_key: bool = False,
                 auto_increment: bool = False,
                 **kwargs):
        self.name = name
        self.type = type
        self.nullable = nullable
        self.default = default
        self.kwargs = kwargs
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        self.type_param = type_param

    def get_params(self) -> dict[str, Union[str, int, float, bool]]:
        return self.kwargs

    def get_type_col(self) -> str:
        return self.TYPES.get(self.type)

    def render(self) -> str:
        kw = self.get_params()
        params = ', '.join([f"{k}='{v}'" if isinstance(v, str) else f'{k}={v}'
                            for k, v in kw.items()])
        type_col = self.get_type_col()
        type_params = str(self.type_param) if 'int' not in self.type else None
        p = [type_params, params]
        return f'{self.name} = {type_col}({", ".join([i for i in p if i and i != "None"])})'


class CreateTableSQLToModel:

    def __init__(self, column_cls: Type[Column]):
        self.column_cls = column_cls

    def __call__(self, sql: str, module_name: str = None):
        table_name, content = self.parse_model(sql)
        print(content)
        return table_name, content

    def parse_model(self, sql: str) -> tuple[str, str]:
        tablename, columns = self.parse_sql(sql)
        model_name = underline_to_camel_case(tablename)

        ret = f"""class {model_name}({self.column_cls.BASE_CLS}):"""
        for col in columns:
            ret += f'\n    {col.render()}'

        return tablename, ret

    def parse_sql(self, sql: str) -> Tuple[str, List[Column]]:
        sql = sql.lower()
        sql = sql.replace('\r', '').replace('\n', '')
        ret = re.findall(r'create table (.*?) ', sql)
        table_name = remove_quote(ret[0])

        ret = re.findall(r'\(.*\)', sql)
        content = ret[0].strip()[1:-1]
        columns = content.split(',')
        primary_key = 'id'
        columns_ = []
        for col in columns:
            try:
                if 'primary key' in col:
                    primary_key = remove_quote(re.findall(r'\((.*?)\)', col)[0])
                    continue

                col = col.strip()
                col_params = col.split(' ')
                name = remove_quote(col_params[0])
                if name in KEYS:
                    continue

                type, type_param = self.get_type(col_params[1])
                column = self.column_cls(name, type, type_param)
                if 'not null' in col:
                    column.nullable = False

                if 'default' in col:
                    column.default = remove_quote(col_params[col_params.index('default') + 1])

                if 'auto_increment' in col:
                    column.auto_increment = True

                columns_.append(column)
            except:
                print(traceback.format_exc())
                print(f'{col} 解析失败')

        for col in columns_:
            if col.name == primary_key:
                col.primary_key = True

        return table_name, columns_

    def get_type(self, val: str) -> Tuple[str, Any]:
        ret = re.findall(r'(.*?)\((.*?)\)', val)
        if not ret:
            return val, None

        type, param = ret[0]
        param: str = param
        return type, int(param) if param.isalnum() else param


def remove_quote(val: str) -> str:
    val = val.strip()
    if val[0] == val[-1] and val[0] in """'"`""":
        return val[1:-1]
    return val
