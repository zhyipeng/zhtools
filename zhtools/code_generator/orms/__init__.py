from .generator import CreateTableSQLToModel
from .sqlalchemy import SqlalchemyColumn
from .tortoise import TortoiseColumn

tortoise_orm = CreateTableSQLToModel(TortoiseColumn)
sqlalchemy_orm = CreateTableSQLToModel(SqlalchemyColumn)
