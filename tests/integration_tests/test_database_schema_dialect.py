import os
from unittest import TestCase

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from colorama import Fore
from dotenv import load_dotenv

from camel_database_agent.database.database_manager import DatabaseManager
from camel_database_agent.database.dialect.database_schema_dialect import (
    DatabaseSchemaDialect,
)
from camel_database_agent.database.dialect.database_schema_dialect_sqlite import (
    DatabaseSchemaDialectSqlite,
)

load_dotenv("../../.env")  # isort:skip


class TestDatabaseSchemaDialect(TestCase):
    dialect: DatabaseSchemaDialect

    @classmethod
    def setUpClass(cls) -> None:
        model = ModelFactory.create(
            model_platform=ModelPlatformType.DEFAULT,
            model_type=ModelType.DEFAULT,
        )
        database_manager = DatabaseManager(db_url="sqlite:///:memory:")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "ddl.sql"), "r") as f:
            database_manager.execute(f.read(), ignore_sql_check=True)
        with open(os.path.join(current_dir, "data.sql"), "r") as f:
            database_manager.execute(f.read(), ignore_sql_check=True)

        DatabaseSchemaDialect.register(DatabaseSchemaDialectSqlite)

        cls.dialect = DatabaseSchemaDialect.get_dialect(
            dialect_name=database_manager.dialect_name(),
            database_manager=database_manager,
            model=model,
        )

    def test_get_schema(self) -> None:
        ddl_sql = self.dialect.get_schema()
        print(Fore.GREEN + ddl_sql)
        assert ddl_sql is not None

        polished_ddl_sql = self.dialect.get_polished_schema()
        print(Fore.BLUE + polished_ddl_sql)
        assert polished_ddl_sql is not None
        assert ddl_sql != polished_ddl_sql

    def test_sampled_data(self) -> None:
        sample_sql = self.dialect.get_sampled_data()
        print(Fore.GREEN + sample_sql)
        assert sample_sql is not None
