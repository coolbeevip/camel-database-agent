import os
from unittest import TestCase

from dotenv import load_dotenv

from camel_database_agent.database.database_manager import DatabaseManager, SQLExecutionError

load_dotenv()  # isort:skip


class TestDatabaseManager(TestCase):
    database_manager: DatabaseManager

    @classmethod
    def setUpClass(cls) -> None:
        cls.database_manager = DatabaseManager(db_url="sqlite:///:memory:")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, "ddl.sql"), "r") as f:
            cls.database_manager.execute(f.read(), ignore_sql_check=True)
        with open(os.path.join(current_dir, "data.sql"), "r") as f:
            cls.database_manager.execute(f.read(), ignore_sql_check=True)

    def test_select_with_fail(self) -> None:
        sql = "select * from no_exist_table"
        result = self.database_manager.select(sql)
        assert isinstance(result, SQLExecutionError)
        assert result.sql == sql
