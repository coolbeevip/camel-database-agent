import abc
import logging
from typing import ClassVar, List, Optional, Type, TypeVar, Union

from camel.agents import ChatAgent
from camel.models import BaseModelBackend

from camel_database_agent.database.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="DatabaseSchemaDialect")


class DatabaseSchemaDialect(abc.ABC):
    dialect_name: str
    dialect_map: ClassVar[dict[str, Type["DatabaseSchemaDialect"]]] = {}
    schema_polish_agent: ChatAgent
    schema: str

    def __init__(
        self,
        database_manager: DatabaseManager,
        model: Optional[Union[BaseModelBackend, List[BaseModelBackend]]] = None,
    ):
        self.database_manager = database_manager
        if model:
            self.schema_polish_agent = ChatAgent(
                system_message="You are a database expert, proficient in the "
                "SQL syntax of various databases.",
                model=model,
            )

    @classmethod
    def register(cls, dialect_type: Type[T]) -> Type[T]:
        if not issubclass(dialect_type, DatabaseSchemaDialect):
            raise TypeError(f"Expected subclass of DatabaseSchemaDialect, got {dialect_type}")
        cls.dialect_map[dialect_type.dialect_name] = dialect_type
        return dialect_type

    @classmethod
    def get_dialect(
        cls,
        dialect_name: str,
        database_manager: DatabaseManager,
        model: Optional[Union[BaseModelBackend, List[BaseModelBackend]]] = None,
    ) -> "DatabaseSchemaDialect":
        dialect_type: Type["DatabaseSchemaDialect"] = cls.dialect_map[dialect_name]
        return dialect_type(database_manager=database_manager, model=model)

    def get_polished_schema(self, language: str = "English") -> str:
        if self.schema_polish_agent:
            prompt = (
                f"Please optimize the SQL schema of the database in {language}, "
                f"ensuring it includes table name comments, field comments, "
                f"foreign key explanations, etc., to make it more readable.\n\n"
            )
            prompt += f"```sql\n{self.get_schema()}```\n\n"
            prompt += (
                "Now, please directly output the optimized SQL Schema. "
                "Do not explain the process and optimization ideas."
            )
            response = self.schema_polish_agent.step(prompt)
            return response.msgs[0].content
        else:
            return self.get_schema()

    @abc.abstractmethod
    def get_schema(self) -> str:
        """
        Abstract method that returns the database schema as a string.
        Must be implemented by all dialect subclasses.
        """
        pass

    @abc.abstractmethod
    def get_table_names(self) -> List[str]:
        """
        Abstract method that returns the table names in the database.
        Must be implemented by all dialect subclasses.
        """
        pass

    def get_sampled_data(self, data_samples_size: int = 5) -> str:
        """
        Abstract method that returns sampled data from the database as a string.
        Must be implemented by all dialect subclasses.
        """
        metadata = self.database_manager.get_metadata()
        sample_data_sql = []

        for table_name in metadata.tables:
            table = metadata.tables[table_name]
            column_names = [column.name for column in table.columns]

            sample_query = f"SELECT * FROM {table_name} LIMIT {data_samples_size}"
            try:
                rows = self.database_manager.select(sample_query)
                for row in rows:
                    columns = []
                    values = []

                    for col_name in column_names:
                        if col_name in row and row[col_name] is not None:
                            columns.append(col_name)
                            if isinstance(row[col_name], str):
                                values.append("'" + row[col_name].replace("'", "''") + "'")
                            elif isinstance(row[col_name], (int, float)):
                                values.append(str(row[col_name]))
                            else:
                                values.append(f"'{row[col_name]!s}'")

                    if columns and values:
                        columns_stmt = ', '.join(columns)
                        values_stmt = ', '.join(values)
                        insert_stmt = (
                            f"INSERT INTO {table_name} ({columns_stmt}) VALUES ({values_stmt});"
                        )
                        sample_data_sql.append(insert_stmt)

            except Exception as e:
                logger.warning(f"Error sampling data from table {table_name}: {e}")

        return "\n".join(sample_data_sql)
