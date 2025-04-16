import os
from unittest import TestCase

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from dotenv import load_dotenv

from camel_database_agent.database.manager import DatabaseManager
from camel_database_agent.database.schema import (
    DatabaseSchemaParse,
    SchemaParseResponse,
)

load_dotenv("../../.env")  # isort:skip


class TestDatabaseSchemaParse(TestCase):
    parse: DatabaseSchemaParse

    @classmethod
    def setUpClass(cls) -> None:
        model = ModelFactory.create(
            model_platform=ModelPlatformType.DEFAULT,
            model_type=ModelType.DEFAULT,
        )
        cls.parse = DatabaseSchemaParse(
            database_manager=DatabaseManager(db_url="sqlite:///:memory:"),
            model=model,
        )

    def test_parse_ddl_record(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "ddl.sql"), "r") as f:
            schema_parse_response: SchemaParseResponse = self.parse.parse_ddl_record(f.read())
            assert len(schema_parse_response.data) == 6

    def test_parse_dml_record(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "data.sql"), "r") as f:
            schema_parse_response: SchemaParseResponse = self.parse.parse_sampled_record(f.read())
            assert len(schema_parse_response.data) == 6

    def test_parse_query_record(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "query.md"), "r") as f:
            schema_parse_response: SchemaParseResponse = self.parse.parse_query_record(f.read())
            assert len(schema_parse_response.data) == 3
