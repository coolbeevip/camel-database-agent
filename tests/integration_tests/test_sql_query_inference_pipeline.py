import os
from unittest import TestCase

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from dotenv import load_dotenv

from camel_database_agent import DataQueryInferencePipeline
from camel_database_agent.database.database_manager import DatabaseManager

load_dotenv("../../.env")  # isort:skip


class TestDataQueryInferencePipeline(TestCase):
    pipeline: DataQueryInferencePipeline

    @classmethod
    def setUpClass(cls) -> None:
        database_manager = DatabaseManager(db_url="sqlite:///:memory:")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "ddl.sql"), "r") as f:
            ddl_sql = f.read()
            database_manager.execute(ddl_sql, ignore_sql_check=True)
        with open(os.path.join(current_dir, "data.sql"), "r") as f:
            data_sql = f.read()
            database_manager.execute(data_sql, ignore_sql_check=True)

        cls.pipeline = DataQueryInferencePipeline(
            ddl_sql=ddl_sql,
            data_sql=data_sql,
            model=ModelFactory.create(
                model_platform=ModelPlatformType.DEFAULT,
                model_type=ModelType.DEFAULT,
            ),
            database_manager=database_manager,
        )

    def test_generate(self) -> None:
        query_records = self.pipeline.generate(10)
        assert len(query_records) == 10
