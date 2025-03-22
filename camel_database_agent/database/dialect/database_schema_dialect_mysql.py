from typing import ClassVar, List, Optional, Union

from camel.models import BaseModelBackend
from sqlalchemy import text

from camel_database_agent.database.database_manager import (
    DatabaseManager,
)
from camel_database_agent.database.dialect.database_schema_dialect import (
    DatabaseSchemaDialect,
)


class DatabaseSchemaDialectMySQL(DatabaseSchemaDialect):
    dialect_name = "mysql"
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
            result = database_manager.select(text(f"SHOW CREATE TABLE {table.name}"))
            row = result.fetchone()
            create_table = row[1] if row else ""
            ddl_statements.append(create_table + ";")
        self.schema = "\n".join(ddl_statements)

    def get_schema(self) -> str:
        return self.schema

    def get_table_names(self) -> List[str]:
        return self.table_names


DatabaseSchemaDialect.register(DatabaseSchemaDialectMySQL)
