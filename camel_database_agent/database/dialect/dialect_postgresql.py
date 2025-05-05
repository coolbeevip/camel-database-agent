# Copyright 2025 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import ClassVar, List, Optional, Union

from camel.models import BaseModelBackend

from camel_database_agent.database.dialect.dialect import (
    DatabaseSchemaDialect,
)
from camel_database_agent.database.manager import DatabaseManager


class DatabaseSchemaDialectPostgresql(DatabaseSchemaDialect):
    dialect_name = "postgresql"
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
            create_stmt = [f"CREATE TABLE {table.name} ("]
            columns = []
            for column in table.columns:
                col_def = f"    {column.name} {column.type}"
                if not column.nullable:
                    col_def += " NOT NULL"
                if column.primary_key:
                    col_def += " PRIMARY KEY"
                if column.server_default:
                    if hasattr(column.server_default, "arg"):
                        col_def += f" DEFAULT {column.server_default.arg}"
                    else:
                        col_def += f" DEFAULT {column.server_default}"
                columns.append(col_def)
            create_stmt.append(",\n".join(columns))
            create_stmt.append(");")

            # 获取表注释
            result = self.database_manager.select(
                f"SELECT obj_description('{table.name}'::regclass, 'pg_class')"
            )
            table_comment = result[0]['obj_description']
            if table_comment:
                create_stmt.append(f"COMMENT ON TABLE {table.name} IS '{table_comment}';")

            # 获取列注释
            for column in table.columns:
                result = self.database_manager.select(
                    f"SELECT col_description('{table.name}'::regclass, "
                    f"(SELECT ordinal_position FROM information_schema.columns "
                    f"WHERE table_name = '{table.name}' AND column_name = '{column.name}'))"
                )
                col_comment = result[0]['col_description']
                if col_comment:
                    create_stmt.append(
                        f"COMMENT ON COLUMN {table.name}.{column.name} IS '{col_comment}';"
                    )

            ddl_statements.append("\n".join(create_stmt))
        self.schema = "\n".join(ddl_statements)

    def get_schema(self) -> str:
        return self.schema

    def get_table_names(self) -> List[str]:
        return self.table_names


DatabaseSchemaDialect.register(DatabaseSchemaDialectPostgresql)
