import json
import logging
import os
import random
from typing import Any, List, Optional, Union

from camel.agents import BaseAgent, ChatAgent
from camel.embeddings import BaseEmbedding, OpenAIEmbedding
from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType, ModelType
from colorama import Fore
from pydantic import BaseModel
from tabulate import tabulate

from camel_database_agent.database.database_manager import DatabaseManager
from camel_database_agent.database.database_schema_parse import (
    DatabaseSchemaParse,
    DDLRecord,
    DMLRecord,
    QueryRecord,
)
from camel_database_agent.database.dialect.database_schema_dialect import (
    DatabaseSchemaDialect,
)
from camel_database_agent.database_base import (
    AssistantMessage,
    HumanMessage,
    MessageLog,
    MessageLogToEmpty,
    SQLExecutionError,
    TrainLevel,
    messages_log,
    strip_sql_code_block,
    timing,
)
from camel_database_agent.database_prompt import (
    DATABASE_SUMMARY_OUTPUT_EXAMPLE,
    QUESTION_CONVERT_SQL,
)
from camel_database_agent.datagen.sql_query_inference_pipeline import (
    DataQueryInferencePipeline,
)
from camel_database_agent.knowledge.database_knowledge import DatabaseKnowledge, RecordType
from camel_database_agent.knowledge.database_knowledge_qdrant import (
    DatabaseKnowledgeQdrant,
)

logger = logging.getLogger(__name__)


class QuestionMeta(BaseModel):
    question: str
    sql: str
    prompt: str
    usage: dict


class DatabaseAgentResponse(BaseModel):
    ask: str
    dataset: Optional[Any] = None
    sql: Optional[str] = None
    success: bool = True
    error: Optional[str] = None
    usage: Optional[dict] = None


class DatabaseAgent(BaseAgent):
    database_summary: str = ""
    recommendation_question: str = ""

    def step(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def reset(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def __init__(
        self,
        db_url: Optional[str] = None,
        ddl_sql: Optional[str] = None,
        data_sql: Optional[str] = None,
        polished_schema: bool = True,
        database_manager: Optional[DatabaseManager] = None,
        model: Optional[Union[BaseModelBackend, List[BaseModelBackend]]] = None,
        embedding_model: Optional[BaseEmbedding] = None,
        database_knowledge: Optional[DatabaseKnowledge] = None,
        data_path: Optional[str] = None,
        language: str = "English",
        interactive_mode: bool = False,
        read_only_model: bool = True,
    ):
        self.interactive_mode = interactive_mode
        if database_manager:
            self.database_manager = database_manager
        else:
            if db_url:
                self.database_manager = DatabaseManager(
                    db_url=db_url, read_only_model=read_only_model
                )
            else:
                raise ValueError("db_url or database_manager must be provided")
        self.ddl_sql = ddl_sql
        self.data_sql = data_sql
        self.language = language
        if not data_path:
            user_home = os.path.expanduser("~")
            data_path = os.path.join(user_home, "camel_database_agent_data")
            if not os.path.exists(data_path):
                os.makedirs(data_path)
        logger.info(f"Workspace: {data_path}")
        self.data_path = data_path
        self.polished_schema = polished_schema
        self.model_backend = (
            model
            if model
            else ModelFactory.create(
                model_platform=ModelPlatformType.DEFAULT,
                model_type=ModelType.DEFAULT,
            )
        )
        self.embedding_model_backend = embedding_model if embedding_model else OpenAIEmbedding()
        self.knowledge_path = os.path.join(str(self.data_path), "knowledge")
        self.database_knowledge_backend = (
            database_knowledge
            if database_knowledge
            else DatabaseKnowledgeQdrant(
                embedding=self.embedding_model_backend,
                model=self.model_backend,
                path=self.knowledge_path,
            )
        )
        self.dialect: DatabaseSchemaDialect = DatabaseSchemaDialect.get_dialect(
            dialect_name=self.database_manager.dialect_name(),
            database_manager=self.database_manager,
            model=self.model_backend,
        )
        self.schema_parse = DatabaseSchemaParse(
            database_manager=self.database_manager, model=self.model_backend
        )
        self.agent = ChatAgent(
            system_message="You are a business expert, skilled at in-depth "
            "analysis of user data query requirements through "
            "reverse engineering of database table structures.",
            model=self.model_backend,
            message_window_size=100,
        )
        if os.path.exists(os.path.join(self.knowledge_path, "database_summary.txt")):
            with open(
                os.path.join(self.knowledge_path, "database_summary.txt"),
                "r",
                encoding="utf-8",
            ) as f:
                self.database_summary = f.read()
        if os.path.exists(os.path.join(self.knowledge_path, "recommendation_question.txt")):
            with open(
                os.path.join(self.knowledge_path, "recommendation_question.txt"),
                "r",
                encoding="utf-8",
            ) as f:
                self.recommendation_question = f.read()
        if self.ddl_sql is None and os.path.exists(
            os.path.join(self.knowledge_path, "ddl_sql.sql")
        ):
            with open(
                os.path.join(self.knowledge_path, "ddl_sql.sql"),
                "r",
                encoding="utf-8",
            ) as f:
                self.ddl_sql = f.read()
        if self.data_sql is None and os.path.exists(
            os.path.join(self.knowledge_path, "data_sql.sql")
        ):
            with open(
                os.path.join(self.knowledge_path, "data_sql.sql"),
                "r",
                encoding="utf-8",
            ) as f:
                self.data_sql = f.read()

    @timing
    def _parse_schema_to_knowledge(self, polish: bool = False) -> None:
        """Generate schema data to knowledge"""
        self.ddl_sql = (
            self.dialect.get_polished_schema(self.language)
            if polish
            else self.dialect.get_schema()
        )
        # Save the schema to a file
        with open(
            os.path.join(self.knowledge_path, "ddl_origin.sql"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.dialect.get_schema())

        # Save the polished schema to a file
        with open(
            os.path.join(self.knowledge_path, "ddl_sql.sql"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.ddl_sql)

        ddl_records: List[DDLRecord] = self.schema_parse.parse_ddl_record(self.ddl_sql)
        with open(
            os.path.join(self.knowledge_path, "ddl_records.json"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                json.dumps(
                    [record.model_dump() for record in ddl_records], ensure_ascii=False, indent=4
                )
            )

        self.database_knowledge_backend.add(ddl_records)

    @timing
    def _parse_sampled_data_to_knowledge(self, data_samples_size: int = 5) -> None:
        """Generate sampled data to knowledge"""
        self.data_sql = self.dialect.get_sampled_data(data_samples_size=data_samples_size)
        with open(
            os.path.join(self.knowledge_path, "data_sql.sql"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.data_sql)
        dml_records: List[DMLRecord] = self.schema_parse.parse_dml_record(self.data_sql)

        with open(
            os.path.join(self.knowledge_path, "data_records.json"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(
                json.dumps(
                    [record.model_dump() for record in dml_records], ensure_ascii=False, indent=4
                )
            )

        self.database_knowledge_backend.add(dml_records)

    @timing
    def _parse_query_to_knowledge(self, query_samples_size: int = 20) -> None:
        """Generate some queries to knowledge"""
        if self.ddl_sql and self.data_sql:
            pipeline = DataQueryInferencePipeline(
                ddl_sql=self.ddl_sql,
                data_sql=self.data_sql,
                model=self.model_backend,
                database_manager=self.database_manager,
                language=self.language,
            )
            query_records: List[QueryRecord] = []
            while len(query_records) < query_samples_size:
                query_records.extend(pipeline.generate(query_samples_size=query_samples_size))

            with open(
                os.path.join(self.knowledge_path, "question_sql.txt"),
                "w",
                encoding="utf-8",
            ) as f:
                for query_record in query_records:
                    f.write(f"QUESTION: {query_record.question}\nSQL: {query_record.sql}\n\n")

            self.database_knowledge_backend.add(query_records)
        else:
            raise ValueError("ddl_sql and data_sql must be provided")

    @timing
    def generate_database_summary(self, query_samples_size: int) -> None:
        self.ddl_sql = (
            self.dialect.get_polished_schema(self.language)
            if not self.polished_schema
            else self.dialect.get_schema()
        )
        query_samples: List[QueryRecord] = (
            self.database_knowledge_backend.get_query_collection_sample(query_samples_size)
        )

        prompt = DATABASE_SUMMARY_OUTPUT_EXAMPLE
        prompt = prompt.replace("{{ddl_sql}}", self.ddl_sql)
        prompt = prompt.replace("{{language}}", self.language)

        response = self.agent.step(prompt)
        self.database_summary = response.msgs[0].content
        with open(
            os.path.join(self.knowledge_path, "database_summary.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.database_summary)
        self.recommendation_question = "\n".join(
            [query_sample.question for query_sample in query_samples]
        )
        with open(
            os.path.join(self.knowledge_path, "recommendation_question.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.recommendation_question)

    def get_summary(self) -> str:
        return self.database_summary

    def get_recommendation_question(self, sampled_num: int = 5) -> str:
        """
        Returns a string with randomly sampled questions from the recommendation_question list.

        Args:
            sampled_num: Number of questions to sample

        Returns:
            A string with sampled questions (one per line)
        """
        questions = self.recommendation_question.strip().split('\n')

        # Ensure we don't try to sample more questions than available
        sampled_num = min(sampled_num, len(questions))

        # Randomly sample questions
        sampled_questions = random.sample(questions, sampled_num)

        return '\n'.join(sampled_questions)

    def add_knowledge(self, records: List[RecordType]) -> None:
        self.database_knowledge_backend.add(records)

    @timing
    def train_knowledge(
        self,
        level: TrainLevel = TrainLevel.MEDIUM,
        reset_train: bool = False,
    ) -> None:
        """Train knowledge"""
        data_samples_size = 20
        table_count = len(self.dialect.get_table_names())
        query_samples_size = table_count
        if level == TrainLevel.LOW:
            query_samples_size = table_count * 2
        elif level == TrainLevel.MEDIUM:
            query_samples_size = table_count * 5
        elif level == TrainLevel.HIGH:
            query_samples_size = table_count * 10

        if reset_train and os.path.exists(self.knowledge_path):
            self.database_knowledge_backend.clear()
            self.ddl_sql = None
            self.data_sql = None
            self.database_summary = ""
            self.recommendation_question = ""
            logger.info("Reset knowledge...")

        if (
            self.database_knowledge_backend.get_table_collection_size() == 0
            or self.database_knowledge_backend.get_data_collection_size() == 0
            or self.database_knowledge_backend.get_query_collection_size() == 0
        ):
            message = (
                f"Initial knowledge base training on {table_count} tables. "
                f"It will take {Fore.GREEN}about {int(table_count * 28 / 60)} minutes.{Fore.RESET}"
            )
            if self.interactive_mode:
                logger.info(f"\r{message}")
            else:
                logger.info(message)

        if self.database_knowledge_backend.get_table_collection_size() == 0:
            self._parse_schema_to_knowledge(polish=self.polished_schema)
        if self.database_knowledge_backend.get_data_collection_size() == 0:
            self._parse_sampled_data_to_knowledge(data_samples_size=data_samples_size)
        if self.database_knowledge_backend.get_query_collection_size() == 0:
            self._parse_query_to_knowledge(query_samples_size)

        if not self.database_summary or reset_train:
            self.generate_database_summary(query_samples_size=query_samples_size)

    @timing
    def question_to_sql(self, question: str, dialect_name: str) -> QuestionMeta:
        """Question to SQL"""
        prompt = QUESTION_CONVERT_SQL.replace("{{dialect_name}}", dialect_name)

        ddl_records: List[DDLRecord] = self.database_knowledge_backend.query_ddl(question)
        prompt = prompt.replace(
            "{{table_schema}}", "\n".join([record.sql for record in ddl_records])
        )

        data_records: List[DMLRecord] = self.database_knowledge_backend.query_data(question)
        prompt = prompt.replace(
            "{{sample_data}}", "\n".join([record.sql for record in data_records])
        )

        query_records: List[QueryRecord] = self.database_knowledge_backend.query_query(question)
        prompt = prompt.replace(
            "{{qa_pairs}}",
            "\n".join(
                [f"QUESTION: {record.question}\nSQL: {record.sql}\n\n" for record in query_records]
            ),
        )

        prompt = prompt.replace("{{question}}", question)
        logger.debug(Fore.GREEN + "PROMPT:" + prompt)
        self.agent.reset()
        response = self.agent.step(prompt)

        return QuestionMeta(
            question=question,
            sql=strip_sql_code_block(response.msgs[0].content),
            prompt=prompt,
            usage=response.info['usage'],
        )

    @messages_log
    def ask(
        self,
        session_id: str,
        question: str,
        message_log: Optional[MessageLog] = None,
        bind_pd: Optional[bool] = True,
    ) -> DatabaseAgentResponse:
        if not message_log:
            message_log = MessageLogToEmpty()
        message_log.messages_writer(HumanMessage(session_id=session_id, content=question))
        question_meta = self.question_to_sql(
            question=question,
            dialect_name=self.database_manager.dialect_name(),
        )
        try:
            message_log.messages_writer(
                AssistantMessage(session_id=session_id, content=question_meta.sql)
            )
            dataset = self.database_manager.select(sql=question_meta.sql, bind_pd=bind_pd)
            message_log.messages_writer(
                AssistantMessage(
                    session_id=session_id,
                    content=tabulate(dataset, headers="keys", tablefmt="psql"),
                )
            )
            return DatabaseAgentResponse(
                ask=question,
                dataset=dataset,
                sql=question_meta.sql,
                usage=question_meta.usage,
            )
        except SQLExecutionError as e:
            message_log.messages_writer(AssistantMessage(session_id=session_id, content=str(e)))
            return DatabaseAgentResponse(
                ask=question,
                dataset=None,
                sql=e.sql,
                success=False,
                error=e.error_message,
                usage=question_meta.usage,
            )
        except Exception as e:
            message_log.messages_writer(AssistantMessage(session_id=session_id, content=str(e)))
            return DatabaseAgentResponse(
                ask=question,
                dataset=None,
                sql=question_meta.sql,
                success=False,
                error=str(e),
            )
