"""
设置 pandas 显示选项
"""

import argparse
import hashlib
import logging
import os
import sys
import uuid
from threading import Event, Thread
from urllib.parse import urlparse

import pandas as pd
from camel.embeddings import OpenAICompatibleEmbedding
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from colorama import Fore
from tabulate import tabulate

from camel_database_agent import DatabaseAgent
from camel_database_agent.database.manager import DatabaseManager
from camel_database_agent.database_agent import DatabaseAgentResponse
from camel_database_agent.database_base import TrainLevel, spinner

"""Logging"""
logging.basicConfig(
    level=logging.ERROR,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
logging.getLogger("camel_database_agent").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

"""Pandas display"""
pd.set_option("display.max_rows", None)  # Show all rows
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", None)  # Auto-detect display width
pd.set_option("display.max_colwidth", None)  # Show full content of each cell


def generate_db_id(db_url: str, language: str) -> str:
    """
    Generate a unique ID from a database URL by hashing relevant parts.

    Args:
        db_url: SQLAlchemy database connection string

    Returns:
        A unique ID string derived from the database connection
    """
    # Parse the database URL
    parsed_url = urlparse(db_url)

    # Extract components that uniquely identify this database
    dialect = parsed_url.scheme
    netloc = parsed_url.netloc
    path = parsed_url.path

    # Create a string with the most important identifying information
    db_identifier = f"{dialect}:{netloc}{path}:{language}"

    # Create a hash of the identifier
    db_hash = hashlib.md5(db_identifier.encode()).hexdigest()

    # Use first 12 characters for a reasonably unique but short ID
    short_id = db_hash[:12]

    return short_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the database using natural language.")
    parser.add_argument(
        "--database-url",
        "-d",
        required=True,
        help="Database URL (e.g., sqlite:///db.sqlite)",
    )
    parser.add_argument(
        "--openai-api-key",
        "-key",
        required=False,
        default=os.environ.get("OPENAI_API_KEY"),
        help="OpenAI KEY",
    )
    parser.add_argument(
        "--openai-api-base-url",
        "-url",
        required=False,
        default=os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
        help="OPENAI API",
    )
    parser.add_argument(
        "--model-name",
        "-em",
        required=False,
        default=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        help="Model name, such as gpt-3.5-turbo or gpt-4o-mini",
    )
    parser.add_argument(
        "--embedd-model-name",
        "-m",
        required=False,
        default=os.environ.get("EMBED_MODEL_NAME", "text-embedding-ada-002"),
        help="Embedding model name, such as text-embedding-ada-002",
    )
    parser.add_argument("--reset-train", "-rt", action="store_true", help="Retraining knowledge")
    parser.add_argument(
        "--read-only", "-ro", action="store_true", default=True, help="SQL Read-Only Model"
    )
    parser.add_argument(
        "--language",
        "-lang",
        required=False,
        default="English",
        help="The language you used to ask the question, such as English or Chinese.",
    )
    parser.add_argument(
        "--timeout",
        required=False,
        default=1800,
        help="The timeout value in seconds for API calls.",
    )
    args = parser.parse_args()

    # Create a data directory for the database agent
    user_home = os.path.expanduser("~")
    data_path = os.path.join(
        user_home, "camel_database_agent_data", generate_db_id(args.database_url, args.language)
    )

    # Create a database manager and database agent
    database_manager = DatabaseManager(db_url=args.database_url)
    database_agent = DatabaseAgent(
        interactive_mode=True,
        database_manager=database_manager,
        model=ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
            model_type=args.model_name,
            api_key=args.openai_api_key,
            url=args.openai_api_base_url,
            timeout=args.timeout,
        ),
        embedding_model=OpenAICompatibleEmbedding(
            api_key=args.openai_api_key,
            url=args.openai_api_base_url,
            model_type=args.embedd_model_name,
        ),
        language=args.language,
        data_path=data_path,
    )
    token_usage = database_agent.train_knowledge(
        level=TrainLevel.MEDIUM,
        reset_train=args.reset_train,
    )

    print(f"{Fore.GREEN}")
    print("=" * 50)
    print(f"{Fore.GREEN}Database Overview")
    print("=" * 50)
    print(f"{database_agent.get_summary()}")
    print("=" * 50)
    print(f"{Fore.LIGHTYELLOW_EX}Recommendation Question")
    print("=" * 50)
    print(f"{database_agent.get_recommendation_question()}{Fore.RESET}")
    print(f"{Fore.CYAN}=" * 50)
    if args.read_only:
        print(f"Interactive Database Agent Query({Fore.GREEN}Read-Only Mode{Fore.RESET})")
    else:
        print(f"Interactive Database Agent Query({Fore.LIGHTRED_EX}Read-Write Model{Fore.RESET})")
    print(f"{Fore.CYAN}Type {Fore.RED}'exit' or 'quit'{Fore.RESET} to end the session")
    print(
        f"{Fore.CYAN}Type {Fore.LIGHTYELLOW_EX}'help'{Fore.RESET} "
        f"to get more recommended questions"
    )
    print(f"{Fore.CYAN}Training completed, using {token_usage.total_tokens} tokens{Fore.RESET}")
    print(f"{Fore.CYAN}=" * 50)

    session_id = str(uuid.uuid4())

    while True:
        user_question = input(f"{Fore.CYAN}Enter your question: {Fore.RESET}")
        user_question = user_question.strip()
        if user_question.lower() in ["exit", "quit"]:
            print(f"{Fore.YELLOW}Exiting interactive mode. Goodbye!{Fore.RESET}")
            break
        if user_question.lower() == "help":
            print(f"{Fore.GREEN}Database Overview")
            print("=" * 50)
            print(f"{database_agent.get_summary()}")
            print(f"{Fore.LIGHTYELLOW_EX}Recommendation Question")
            print("=" * 50)
            print(f"{database_agent.get_recommendation_question()}{Fore.RESET}")
        elif len(user_question) > 0:
            stop_spinner = Event()
            spinner_thread = Thread(target=spinner, args=(stop_spinner, "Thinking..."))
            spinner_thread.daemon = True
            try:
                # Set up and start the spinner in a separate thread
                spinner_thread.start()

                # Ask the database agent
                response: DatabaseAgentResponse = database_agent.ask(
                    session_id=session_id,
                    question=user_question,
                )

                # Stop the spinner (it will clear the line)
                stop_spinner.set()
                spinner_thread.join()

                if response.success:
                    if response.dataset is not None:
                        data = tabulate(
                            tabular_data=response.dataset, headers='keys', tablefmt='psql'
                        )
                        print(f"{Fore.GREEN}{data}{Fore.RESET}")
                    else:
                        print(f"{Fore.GREEN}No results found.{Fore.RESET}")
                    print(f"{Fore.YELLOW}{response.sql}{Fore.RESET}")
                else:
                    print(f"{Fore.RED}+ {response.error}{Fore.RESET}")
                if response.usage:
                    print(
                        f"{Fore.YELLOW}Tokens used: {response.usage['total_tokens']}{Fore.RESET}"
                    )
            except Exception as e:
                # Make sure to stop the spinner on exception
                if 'stop_spinner' in locals() and not stop_spinner.is_set():
                    stop_spinner.set()
                    spinner_thread.join()
                print(f"{Fore.RED}ERROR: {e}{Fore.RESET}")


if __name__ == "__main__":
    main()
