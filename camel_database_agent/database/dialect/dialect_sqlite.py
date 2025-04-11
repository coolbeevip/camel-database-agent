from typing import ClassVar, List, Optional, Union

from camel.models import BaseModelBackend
from sqlalchemy import DefaultClause

from camel_database_agent.database.dialect.dialect import (
    DatabaseSchemaDialect,
)
from camel_database_agent.database.manager import DatabaseManager


class DatabaseSchemaDialectSqlite(DatabaseSchemaDialect):
    """
    SQLite doesn't support comments in standard DDL, so we use the best approximation
    """

    dialect_name = "sqlite"
    table_names: ClassVar[List[str]] = []

    def __init__(
        self,
        database_manager: DatabaseManager,
        model: Optional[Union[BaseModelBackend, List[BaseModelBackend]]] = None,
    ):
        super().__init__(database_manager=database_manager, model=model)
        ddl_statements = []
        for table in self.database_manager.get_metadata().sorted_tables:
            self.table_names.append(table.name)
            create_stmt = f"CREATE TABLE {table.name} (\n"
            columns = []
            for column in table.columns:
                col_def = f"    {column.name} {column.type}"
                if not column.nullable:
                    col_def += " NOT NULL"
                if column.primary_key:
                    col_def += " PRIMARY KEY"
                if isinstance(column.server_default, DefaultClause):
                    col_def += f" DEFAULT {column.server_default.arg}"
                columns.append(col_def)
            create_stmt += ",\n".join(columns)
            create_stmt += "\n);"
            ddl_statements.append(create_stmt)
        self.schema = "\n".join(ddl_statements)

    def get_schema(self) -> str:
        return self.schema

    def get_table_names(self) -> List[str]:
        return self.table_names


DatabaseSchemaDialect.register(DatabaseSchemaDialectSqlite)
