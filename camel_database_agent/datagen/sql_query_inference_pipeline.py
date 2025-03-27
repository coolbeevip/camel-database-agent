import logging
from typing import List, Optional, Union

from camel.agents import ChatAgent
from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType, ModelType
from colorama import Fore

from camel_database_agent.database.database_manager import DatabaseManager
from camel_database_agent.database.database_schema_parse import (
    QueryRecord,
    QueryRecordResponseFormat,
)
from camel_database_agent.database_base import SQLExecutionError, timing
from camel_database_agent.database_prompt import QUESTION_INFERENCE_PIPELINE

logger = logging.getLogger(__name__)


class DataQueryInferencePipeline:
    def __init__(
        self,
        ddl_sql: str,
        data_sql: str,
        database_manager: DatabaseManager,
        model: Optional[Union[BaseModelBackend, List[BaseModelBackend]]] = None,
        language: str = "English",
    ):
        self.model_backend = (
            model
            if model
            else ModelFactory.create(
                model_platform=ModelPlatformType.DEFAULT,
                model_type=ModelType.DEFAULT,
            )
        )
        self.ddl_sql = ddl_sql
        self.data_sql = data_sql
        self.database_manager = database_manager
        self.question_agent = ChatAgent(
            system_message="You are a business expert, skilled at deeply "
            "analyzing user data query requirements based on "
            "database table structures.",
            model=model,
            output_language=language,
        )

    @timing
    def generate(self, query_samples_size: int = 20) -> List[QueryRecord]:
        """Data generation for samples"""
        dataset: List[QueryRecord] = []
        # Generate samples until we have enough
        error_query_records: List[QueryRecord] = []
        while len(dataset) < query_samples_size:
            prompt = QUESTION_INFERENCE_PIPELINE.replace("{{ddl_sql}}", self.ddl_sql)
            prompt = prompt.replace("{{data_sql}}", self.data_sql)
            prompt = prompt.replace(
                "{{query_samples_size}}", str(query_samples_size - len(dataset))
            )

            response = self.question_agent.step(prompt, response_format=QueryRecordResponseFormat)
            content = response.msgs[0].content.strip()

            if content.startswith("```json") or content.startswith("```"):
                content = content.split("\n", 1)[1]  # Remove first line with ```json
            if content.endswith("```"):
                content = content.rsplit("\n", 1)[0]  # Remove last line with ```
            try:
                structured_response = QueryRecordResponseFormat.model_validate_json(content)
                for item in structured_response.items:
                    try:
                        self.database_manager.select(item.sql)
                        dataset.append(item)
                    except SQLExecutionError as e:
                        # TODO Failed questions and SQL need to be regenerated
                        logger.error(
                            f"{Fore.RED}SQLExecutionError{Fore.RESET}: {e.sql} {e.error_message}"
                        )
                        error_query_records.append(item)
                    except Exception as e:
                        logger.error(f"Error executing query: {item.question} {item.sql} {e!s}")
                        continue
                    finally:
                        logger.info(
                            f"Generation samples collected "
                            f"{Fore.GREEN}{len(dataset)}/{query_samples_size}{Fore.RESET}"
                        )
            except Exception as e:
                logger.error(f"Error parsing response: {e}")
                logger.debug(f"Raw content that caused error: {content[:200]}...")

        return dataset[:query_samples_size]
