
# CAMEL DatabaseAgent

An open-source toolkit helping developers build natural language database query solutions based on [CAMEL](https://github.com/camel-ai/camel).

## Core Components

- **DataQueryInferencePipeline**: A pipeline that transforms database schema and sample data into query few-shot examples (questions and corresponding SQL)
- **DatabaseKnowledge**: A vector database storing database schema, sample data, and query few-shot examples
- **DatabaseAgent**: An intelligent agent based on the CAMEL framework that utilizes DatabaseKnowledge to answer user questions

Current Support Status

- ✅ Read-Only mode
- ✅ SQLite support
- ⏳ MySQL support (in development)  
- ⏳ PostgreSQL support (in development)  
- ⏳ Spider 2.0-Lite evaluation (planned)

## Quick Start

Clone the repository and install the dependencies.

```shell
git clone git@github.com:coolbeevip/camel-database-agent.git
cd camel-database-agent
pip install uv ruff mypy
uv venv .venv --python=3.10
source .venv/bin/activate
uv pip install -e ".[dev,test]"
````

#### Music Database

> This database serves as a comprehensive data model for a digital music distribution platform, encompassing various aspects of artist management, customer interactions, and sales transactions.

Connect to `database/sqlite/music.sqlite` database and use `openai` API to answer questions.

**NOTE: The first connection will take a few minutes to generate knowledge data.**

```shell
source .venv/bin/activate
export OPENAI_API_KEY=sk-xxx
export OPENAI_API_BASE_URL=https://api.openai.com/v1/
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

#### Demo Video

[![CAMEL DatabaseAgent Demo](docs/demo_video.jpg)](https://youtu.be/Fl065DB8Wqo "Watch the CAMEL DatabaseAgent Demo")

## Command Line Options

> usage: cli.py [-h] --database-url DATABASE_URL [--openai-api-key OPENAI_API_KEY] [--openai-api-base-url OPENAI_API_BASE_URL] [--reset-train] [--read-only] [--language LANGUAGE]

* database-url: The database [URLs](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls) to connect to.
* openai-api-key: The OpenAI API key.
* openai-api-base-url: The OpenAI API base URL(default is https://api.openai.com/v1/).
* reset-train: Reset the training data.
* read-only: Read-only mode.
* language: Language used to generate training data.

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
export API_KEY=sk-xx
python spider2_run.py
```

## Development

Install the development dependencies.
```shell
pip install uv ruff mypy
uv pip install -e ".[dev]"
```

Run code formatters
```shell
make format
```

Run code linters
```shell
make lint
```

Run unit tests
```shell
make test
```

Create a uv.lock file from pyproject.toml
```shell
uv pip compile pyproject.toml -o uv.lock --resolution=highest
```