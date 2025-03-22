import os
import uuid
from unittest import TestCase

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from dotenv import load_dotenv

from camel_database_agent import DatabaseAgent
from camel_database_agent.database.database_manager import DatabaseManager
from camel_database_agent.database_base import MessageLogToEmpty

load_dotenv("../../.env")  # isort:skip


class TestDatabaseAgent(TestCase):
    database_manager: DatabaseManager

    @classmethod
    def setUpClass(cls) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cls.database_manager = DatabaseManager(db_url="sqlite:///:memory:")
        with open(os.path.join(current_dir, "ddl.sql"), "r") as f:
            cls.database_manager.execute(f.read(), ignore_sql_check=True)
        with open(os.path.join(current_dir, "data.sql"), "r") as f:
            cls.database_manager.execute(f.read(), ignore_sql_check=True)

    def test_ask(self) -> None:
        database_agent = DatabaseAgent(
            database_manager=self.database_manager,
            model=ModelFactory.create(
                model_platform=ModelPlatformType.DEFAULT,
                model_type=ModelType.DEFAULT,
            ),
            language="Chinese",
        )

        database_agent.train_knowledge(reset_train=True)
        database_agent.ask(
            session_id=str(uuid.uuid4()),
            question="查询最近30天内成功支付用户的订单详情,包括用户信息、订单信息、支付状态、订单明细以及收货地址",
            message_log=MessageLogToEmpty(),
        )
