import logging
import os
import sys
import uuid

import pandas as pd
from camel.embeddings import OpenAIEmbedding
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from colorama import Fore
from tabulate import tabulate

from camel_database_agent import DatabaseAgent
from camel_database_agent.database.database_manager import DatabaseManager
from camel_database_agent.database_base import TrainLevel

# Configure logging settings to show errors on stdout
logging.basicConfig(
    level=logging.ERROR,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)
# Set specific logging level for the application module
logging.getLogger("camel_database_agent").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Configure pandas display options to show complete data
pd.set_option("display.max_rows", None)  # Show all rows
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", None)  # Auto-detect display width
pd.set_option("display.max_colwidth", None)  # Show full content of each cell

# Define database connection string
database_url = "sqlite:///database/sqlite/music.sqlite"

# Initialize the database agent with required components
database_agent = DatabaseAgent(
    interactive_mode=True,
    database_manager=DatabaseManager(db_url=database_url),
    # Configure LLM model
    model=ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI,
        model_type=ModelType.GPT_4O_MINI,
        api_key=os.getenv("OPENAI_API_KEY"),
        url=os.getenv("OPENAI_API_BASE_URL"),
    ),
    # Configure embedding model
    embedding_model=OpenAIEmbedding(
        api_key=os.getenv("OPENAI_API_KEY"),
        url=os.getenv("OPENAI_API_BASE_URL"),
    ),
)

# Train agent's knowledge about the database schema
database_agent.train_knowledge(
    # Training level for database knowledge extraction
    # MEDIUM level: Balances training time and knowledge depth by:
    #  - Analyzing schema relationships
    #  - Extracting representative sample data
    #  - Generating a moderate number of query examples
    level=TrainLevel.MEDIUM,
    # Whether to retrain the knowledge base from scratch
    # If True: Forces regeneration of all database insights and examples
    # If False: Uses existing cached knowledge if available
    reset_train=False,
)

# Display database overview information
print(f"{Fore.GREEN}Database Overview")
print("=" * 50)
print(f"{database_agent.get_summary()}\n\n{Fore.RESET}")

# Display recommended example questions
print(f"{Fore.GREEN}Recommendation Question")
print("=" * 50)
print(f"{database_agent.get_recommendation_question()}\n\n{Fore.RESET}")

# Execute a sample query using natural language
response = database_agent.ask(
    session_id=str(uuid.uuid4()), question="List all playlists with more than 5 tracks"
)

# Handle and display the query results
if response.success:
    if response.dataset is not None:
        # Format successful results as a table
        data = tabulate(tabular_data=response.dataset, headers='keys', tablefmt='psql')
        print(f"{Fore.GREEN}{data}{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}No results found.{Fore.RESET}")
    # Display the SQL that was generated
    print(f"{Fore.YELLOW}{response.sql}{Fore.RESET}")
else:
    # Display error message if query failed
    print(f"{Fore.RED}+ {response.error}{Fore.RESET}")
