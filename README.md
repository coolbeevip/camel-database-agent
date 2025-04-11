# CAMEL DatabaseAgent

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPi version](https://img.shields.io/pypi/v/camel-database-agent.svg)](https://pypi.org/project/camel-database-agent/)
[![build](https://github.com/coolbeevip/camel-database-agent/actions/workflows/pr.yml/badge.svg)](https://github.com/coolbeevip/camel-database-agent/actions/workflows/pr.yml)

An open-source toolkit helping developers build natural language database query solutions based on [CAMEL-AI](https://github.com/camel-ai/camel).

## Core Components

- **DataQueryInferencePipeline**: A pipeline that transforms database schema and sample data into query few-shot examples (questions and corresponding SQL)
- **DatabaseKnowledge**: A vector database storing database schema, sample data, and query few-shot examples
- **DatabaseAgent**: An intelligent agent based on the CAMEL framework that utilizes DatabaseKnowledge to answer user questions

Features:

- [x] Read-Only mode
- [x] SQLite
- [x] MySQL
- [x] PostgreSQL  
- [ ] Spider 2.0-Lite evaluation (planned)

## Quick Start

Clone the repository and install the dependencies.

```shell
git clone git@github.com:coolbeevip/camel-database-agent.git
cd camel-database-agent
pip install uv ruff mypy
uv venv .venv --python=3.10
source .venv/bin/activate
uv sync --all-extras
````

#### Music Database

> This database serves as a comprehensive data model for a digital music distribution platform, encompassing various aspects of artist management, customer interactions, and sales transactions.

Connect to `database/sqlite/music.sqlite` database and use `openai` API to answer questions.

**NOTE: The first connection will take a few minutes to generate knowledge data.**

```shell
source .venv/bin/activate
export OPENAI_API_KEY=sk-xxx
export OPENAI_API_BASE_URL=https://api.openai.com/v1/
export MODEL_NAME=gpt-4o-mini
export EMBEDD_MODEL_NAME=text-embedding-ada-002
python camel_database_agent/cli.py \
--database-url sqlite:///database/sqlite/music.sqlite
```
![](docs/screenshot-music-database.png)

#### School Scheduling Database

> This database serves as a comprehensive data model for an educational institution, encompassing various aspects of student, faculty, and course management. It includes modules for building management, staff and faculty details, student information, course offerings, and class scheduling

Connect to `database/sqlite/school_scheduling.sqlite` database and use `openai` API to answer questions a Chinese.

```shell
source .venv/bin/activate
export OPENAI_API_KEY=sk-xxx
export OPENAI_API_BASE_URL=https://api.openai.com/v1/
python camel_database_agent/cli.py \
--database-url sqlite:///database/sqlite/school_scheduling.sqlite \
--language Chinese
```

![](docs/screenshot-school-scheduling-database.png)

## Demo Video

[![CAMEL DatabaseAgent Demo](docs/demo_video.png)](https://youtu.be/Fl065DB8Wqo "Watch the CAMEL DatabaseAgent Demo")

## Command Line Options

> usage: cli.py [-h] --database-url DATABASE_URL [--openai-api-key OPENAI_API_KEY] [--openai-api-base-url OPENAI_API_BASE_URL] [--reset-train] [--read-only] [--language LANGUAGE]

* database-url: The database [URLs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) to connect to.
* openai-api-key: The OpenAI API key.
* openai-api-base-url: The OpenAI API base URL(default is https://api.openai.com/v1/).
* reset-train: Reset the training data.
* read-only: Read-only mode.
* language: Language used to generate training data.

## MySQL

Start a MySQL container with the following command:

```shell
docker run -d \
  --name camel_mysql \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=school_scheduling \
  -e MYSQL_USER=camel \
  -e MYSQL_PASSWORD=123456 \
  -p 3306:3306 \
  -v $(pwd)/database/mysql:/docker-entrypoint-initdb.d \
  mysql:9
```

Connect to the MySQL database to answer questions.

```shell
python camel_database_agent/cli.py \
--database-url mysql+pymysql://camel:123456@127.0.0.1:3306/school_scheduling
```

## PostgreSQL

Start a PostgreSQL container with the following command:

```shell
docker run -d \
  --name camel_postgresql \
  -e POSTGRES_USER=camel \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=school_scheduling \
  -p 5432:5432 \
  -v $(pwd)/database/postgresql:/docker-entrypoint-initdb.d \
  postgres:17
```

Connect to the PostgreSQL database to answer questions.

```shell
python camel_database_agent/cli.py \
--database-url postgresql://camel:123456@localhost:5432/school_scheduling
```

## Developer Integration

```python
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
from camel_database_agent.database.manager import DatabaseManager
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
    )
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
response = database_agent.ask(session_id=str(uuid.uuid4()),
                              question="List all playlists with more than 5 tracks")

# Handle and display the query results
if response.success:
    if response.dataset is not None:
        # Format successful results as a table
        data = tabulate(
            tabular_data=response.dataset, headers='keys', tablefmt='psql'
        )
        print(f"{Fore.GREEN}{data}{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}No results found.{Fore.RESET}")
    # Display the SQL that was generated
    print(f"{Fore.YELLOW}{response.sql}{Fore.RESET}")
else:
    # Display error message if query failed
    print(f"{Fore.RED}+ {response.error}{Fore.RESET}")
```

Output

```shell
$ python example.py 
Successfully connected to database: sqlite:///database/sqlite/music.sqlite
Workspace: /Users/zhanglei/camel_database_agent_data
Train knowledge Took 0.1063 seconds
Database Overview
==================================================
This database is designed to support a digital music platform, encompassing key features for artist management, employee administration, customer relations, and sales transactions. 

### Key Features:

1. **Artist and Album Management**: 
   The `Artist` and `Album` tables form the foundation for managing musical artists and their respective albums. Each artist is uniquely identified and can have multiple albums linked to them, allowing for comprehensive tracking of discographies.

2. **Employee and Customer Management**:
   The `Employee` table captures detailed information about staff, including their roles, contact details, and reporting structure, which is essential for organizational management. The `Customer` table holds customer profiles, enabling personalized service and facilitating communication through provided contact information.

3. **Media Type and Genre Classification**:
   The `MediaType` and `Genre` tables classify music tracks, enabling easy filtering and searching for users based on their preferences for specific genres or media types (e.g. digital downloads, CDs). This classification enhances user experience by making music discovery intuitive and engaging.

4. **Track and Playlist Management**: 
   The `Track` table contains detailed attributes for individual music tracks, including duration and pricing. The `Playlist` table allows users to create and manage custom playlists, which can enrich user engagement and retention by providing a personalized listening experience.

5. **Sales Tracking and Invoicing**:
   The `Invoice` and `InvoiceLine` tables keep track of sales transactions, linking customers with the purchases they make. This structure not only supports effective billing through clear associations between invoices and the tracks purchased but also facilitates revenue tracking and financial reporting. The ability to view total sales and detailed line items allows for comprehensive sales analysis.

6. **Flexible Design for Data Relationships**:
   Through the use of foreign keys and relationships, such as the linkage between customers and their respective invoices, the database provides a robust structure for maintaining data integrity. The design ensures that all relevant information is easily accessible, promoting efficient database utilization.

Overall, this database structure provides a complete solution for managing a music platform, supporting critical business functions like customer engagement, sales tracking, and music cataloging. It enables organizations to operate efficiently, ensuring a seamless experience for both customers and internal staff.


Recommendation Question
==================================================
List all playlists with more than 5 tracks.
What are the sales figures for each month in 2009?
Show each artist and the number of albums they've released.
What is the total revenue generated from invoices for each customer?
Which tracks belong to the album 'Ball to the Wall'?


Question to SQL Took 2.8951 seconds
Execute Query SQL Took 0.1036 seconds
+----+--------------+--------------+
|    |   PlaylistId |   TrackCount |
|----+--------------+--------------|
|  0 |            1 |         3290 |
|  1 |            3 |          213 |
|  2 |            5 |         1477 |
|  3 |            8 |         3290 |
|  4 |           10 |          213 |
|  5 |           11 |           39 |
|  6 |           12 |           75 |
|  7 |           13 |           25 |
|  8 |           14 |           25 |
|  9 |           15 |           25 |
| 10 |           16 |           15 |
| 11 |           17 |           26 |
+----+--------------+--------------+
SELECT PlaylistId, COUNT(TrackId) as TrackCount FROM PlaylistTrack GROUP BY PlaylistId HAVING TrackCount > 5;
```

## Spider 2.0-Lite(Planned)

[Spider 2.0-Lite](https://github.com/xlang-ai/Spider2/tree/main/spider2-lite) is a text-to-SQL evaluation framework that includes 547 real enterprise-level database use cases, involving various database systems such as BigQuery, Snowflake, and SQLite, to assess the ability of language models in converting text to SQL in complex enterprise environments.

> This use case attempts to query the SQLite database based on user questions 
> and evaluate whether the SQL executes smoothly (**without assessing data accuracy**).

* spider2_lite/database/local_sqlite - SQLite database file. [Manual download required](spider2_lite/database/README.md).
* spider2_lite/spider2-lite.jsonl - Question and SQL pairs. [Link](https://github.com/xlang-ai/Spider2/blob/main/spider2-lite/spider2-lite.jsonl)
* spider2_lite/spider2_run - Run the Spider 2.0-Lite evaluation.

Run the Spider 2.0-Lite evaluation.

```shell
cd spider2_lite
export OPENAI_API_KEY=sk-xxx
export OPENAI_API_BASE_URL=https://api.openai.com/v1/
export MODEL_NAME=gpt-4o-mini
python spider2_run.py
```