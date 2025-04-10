import logging
import os
import sys
import time
from abc import ABC, abstractmethod
from asyncio import Event
from enum import Enum
from functools import wraps
from itertools import cycle
from threading import Thread
from typing import Any, Callable, TypeVar, cast

from colorama import Fore
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TrainLevel(Enum):
    """Enum class for training levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TokenUsage(BaseModel):
    completion_tokens: int = 0
    prompt_tokens: int = 0
    total_tokens: int = 0

    def add_token(self, usage: "TokenUsage"):
        self.completion_tokens += usage.completion_tokens
        self.prompt_tokens += usage.prompt_tokens
        self.total_tokens += usage.total_tokens


class Message(BaseModel):
    session_id: str
    role: str
    content: str


class HumanMessage(Message):
    role: str = "user"


class AssistantMessage(Message):
    role: str = "assistant"


class MessageLog(ABC):
    @abstractmethod
    def messages_writer(self, message: Message) -> None:
        raise NotImplementedError


class MessageLogToEmpty(MessageLog):
    def messages_writer(self, message: Message) -> None:
        pass


class MessageLogToFile(MessageLog):
    def __init__(self, f: Any):
        self.f = f

    def messages_writer(self, message: Message) -> None:
        self.f.write(message.model_dump_json() + "\n")


class SQLExecutionError(Exception):
    """Exception raised for SQL execution errors.

    Attributes:
        sql -- the SQL statement that caused the error
        error_message -- explanation of the error
    """

    def __init__(self, sql: str, error_message: str):
        self.sql = sql
        self.error_message = error_message
        super().__init__(f"SQL execution error: {error_message}\nSQL: {sql}")


T = TypeVar("T", bound=Callable[..., Any])


def spinner(stop_event, message=""):
    spinner_chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    for char in cycle(spinner_chars):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{Fore.LIGHTGREEN_EX}{message}{char}{Fore.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    # Clear the entire line before exiting
    sys.stdout.write('\r' + ' ' * 100 + '\r')
    sys.stdout.flush()


def timing(func: T) -> T:
    @wraps(func)
    def timing_wrapper(*args: Any, **kwargs: Any) -> Any:
        info = func.__name__
        func_doc = func.__doc__
        if func_doc:
            info = func_doc
        start_time = time.perf_counter()

        stop_spinner = Event()
        spinner_thread = Thread(target=spinner, args=(stop_spinner, "Thinking..."))
        spinner_thread.daemon = True
        try:
            spinner_thread.start()
            result = func(*args, **kwargs)
        finally:
            # sys.stdout.write('\r' + ' ' * 100 + '\r')
            stop_spinner.set()
            spinner_thread.join()
            end_time = time.perf_counter()
            total_time = end_time - start_time
            logger.info(f"\r{info} Took {Fore.GREEN}{total_time:.4f} seconds{Fore.RESET}")
        return result

    return cast(T, timing_wrapper)


def messages_log(func: T) -> T:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        session_path = os.path.join(
            str(args[0].data_path), str(kwargs.get("session_id", "default"))
        )
        if not os.path.exists(session_path):
            os.makedirs(session_path, exist_ok=True)

        with open(os.path.join(session_path, "messages.jsonl"), "a", encoding="utf-8") as f:
            kwargs["message_log"] = MessageLogToFile(f)
            return func(*args, **kwargs)

    return cast(T, wrapper)


def strip_sql_code_block(sql: str) -> str:
    """Remove Markdown SQL code block delimiters from the given string."""
    sql = sql.strip()
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.endswith("```"):
        sql = sql[:-3]
    return sql.strip()  # Add extra strip to remove any whitespace after delimiters
