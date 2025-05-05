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
from camel_database_agent.database.manager import (
    DatabaseManager,
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
            result = database_manager.select(f"SHOW CREATE TABLE {table.name}")
            if result:
                create_table = result[0]["Create Table"]
                ddl_statements.append(create_table + ";")
        self.schema = "\n".join(ddl_statements)

    def get_schema(self) -> str:
        return self.schema

    def get_table_names(self) -> List[str]:
        return self.table_names


DatabaseSchemaDialect.register(DatabaseSchemaDialectMySQL)
