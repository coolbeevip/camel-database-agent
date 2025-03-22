import functools
import logging
from contextlib import contextmanager
from typing import Any, Callable, Iterator, List, TypeVar, Union

import pandas as pd
from sqlalchemy import MetaData, Result, create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from camel_database_agent.database_base import SQLExecutionError, timing

T = TypeVar("T")

logger = logging.getLogger(__name__)

read_only_message = (
    "Operation rejected: This SQL contains statements that "
    "could modify data or schema (DROP, DELETE, UPDATE, etc.)"
    " which is not allowed in read-only mode."
)


@contextmanager
def session_scope(session_maker: sessionmaker) -> Iterator[Session]:
    """Context manager for database session handling."""
    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()


def with_session(func: Callable) -> Callable:
    """Decorator that handles session creation and cleanup."""

    @functools.wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        with session_scope(self.Session) as session:
            return func(self, session, *args, **kwargs)

    return wrapper


class DatabaseManager:
    def __init__(self, db_url: str, read_only_model: bool = True):
        self.db_url = db_url
        self.read_only_model = read_only_model
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        with self.engine.connect():
            logger.info(f"Successfully connected to database: {db_url}")

    @timing
    @with_session
    def select(
        self, session: Session, sql: str, bind_pd: bool = False
    ) -> Union[List[dict], pd.DataFrame, SQLExecutionError]:
        """Execute Query SQL"""
        self._check_sql(sql)
        try:
            result: Result = session.execute(text(sql))
            if bind_pd:
                return pd.DataFrame(result.fetchall(), columns=list(result.keys()))
            else:
                # 转换结果为列表字典格式
                column_names = result.keys()
                rows = [dict(zip(column_names, row)) for row in result]
                return rows
        except OperationalError as e:
            return SQLExecutionError(sql, str(e))

    @with_session
    def execute(
        self, session: Session, sql: Union[str, List[str]], ignore_sql_check: bool = False
    ) -> bool:
        """Execute one or more UPDATE/INSERT/DELETE statements."""
        if not ignore_sql_check:
            self._check_sql(sql)
        if isinstance(sql, str):
            for statement in sql.split(";"):
                if statement.strip():
                    session.execute(text(statement))
        else:
            for statement in sql:
                if statement.strip():
                    session.execute(text(statement.strip()))
        return True

    def dialect_name(self) -> str:
        return self.engine.dialect.name

    def get_metadata(self) -> MetaData:
        self.metadata.reflect(bind=self.engine)
        return self.metadata

    def _check_sql(self, sql: Union[str, List[str]]) -> None:
        """Check if SQL is safe to execute (non-destructive)."""
        if self.read_only_model:
            dangerous_keywords = [
                "DROP",
                "TRUNCATE",
                "DELETE",
                "UPDATE",
                "INSERT",
                "ALTER",
                "CREATE",
                "RENAME",
                "REPLACE",
            ]

            statements = []
            if isinstance(sql, str):
                statements = [stmt.strip().upper() for stmt in sql.split(";") if stmt.strip()]
            else:
                statements = [stmt.strip().upper() for stmt in sql if stmt.strip()]

            for stmt in statements:
                # Check for dangerous operations
                for keyword in dangerous_keywords:
                    if keyword in stmt.split():
                        raise SQLExecutionError('\n'.join(statements), read_only_message)
