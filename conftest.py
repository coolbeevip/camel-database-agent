import os

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
