import os
from typing import List
from unittest import TestCase

from camel.embeddings import OpenAIEmbedding
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from dotenv import load_dotenv

from camel_database_agent import DataQueryInferencePipeline
from camel_database_agent.database.database_manager import DatabaseManager
from camel_database_agent.database.database_schema_parse import (
    DatabaseSchemaParse,
    DDLRecord,
)
from camel_database_agent.knowledge.database_knowledge import DatabaseKnowledge
from camel_database_agent.knowledge.database_knowledge_qdrant import (
    DatabaseKnowledgeQdrant,
)

load_dotenv("../../.env")  # isort:skip


class TestDatabaseKnowledge(TestCase):
    parse: DatabaseSchemaParse
    knowledge: DatabaseKnowledge
    database_manager: DatabaseManager

    @classmethod
    def setUpClass(cls) -> None:
        model = ModelFactory.create(
            model_platform=ModelPlatformType.DEFAULT,
            model_type=ModelType.DEFAULT,
        )
        cls.database_manager = DatabaseManager(db_url="sqlite:///:memory:")
        cls.parse = DatabaseSchemaParse(
            database_manager=cls.database_manager,
            model=model,
        )
        cls.knowledge = DatabaseKnowledgeQdrant(embedding=OpenAIEmbedding(), model=model)

    def test_qdrant_with_ddl(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "ddl.sql"), "r") as f:
            ddl_records: List[DDLRecord] = self.parse.parse_ddl_record(f.read())
            self.knowledge.add(ddl_records)

        ddl_records = self.knowledge.query_ddl("查询用户表中的所有用户信息", top_k=2)
        assert len(ddl_records) == 2

    def test_qdrant_with_query(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "ddl.sql"), "r") as f:
            ddl_sql = f.read()
            self.database_manager.execute(ddl_sql, ignore_sql_check=True)
        with open(os.path.join(current_dir, "data.sql"), "r") as f:
            data_sql = f.read()
            self.database_manager.execute(data_sql, ignore_sql_check=True)

        pipeline = DataQueryInferencePipeline(
            ddl_sql=ddl_sql,
            data_sql=data_sql,
            model=ModelFactory.create(
                model_platform=ModelPlatformType.DEFAULT,
                model_type=ModelType.DEFAULT,
            ),
            database_manager=self.database_manager,
        )
        query_records = pipeline.generate(10)
        self.knowledge.add(records=query_records)
        query_records = self.knowledge.get_query_collection_sample(5)
        assert len(query_records) == 5
