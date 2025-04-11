import logging
from typing import List, Optional, Union

from camel.agents import ChatAgent
from camel.models import BaseModelBackend, ModelFactory
from camel.types import ModelPlatformType, ModelType
from colorama import Fore

from camel_database_agent.core.exceptions import QueryParsingError
from camel_database_agent.database.manager import DatabaseManager
from camel_database_agent.database.schema import (
    QueryRecord,
    QueryRecordResponseFormat,
    SchemaParseResponse,
)
from camel_database_agent.database_base import SQLExecutionError, timing
from camel_database_agent.datagen.prompts import PromptTemplates

logger = logging.getLogger(__name__)


class DataQueryInferencePipeline:
    def __init__(
        self,
        ddl_sql: str,
        data_sql: str,
        database_manager: DatabaseManager,
        model: Optional[Union[BaseModelBackend, List[BaseModelBackend]]] = None,
        language: str = "English",
        prompt_templates: Optional[PromptTemplates] = None,
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
        self.prompt_templates = prompt_templates or PromptTemplates()
        self.question_agent = ChatAgent(
            system_message="You are a business expert, skilled at deeply "
            "analyzing user data query requirements based on "
            "database table structures.",
            model=model,
            output_language=language,
        )

    def _prepare_prompt(self, query_samples_needed: int) -> str:
        """Prepare the prompt words for generating queries."""
        prompt = self.prompt_templates.QUESTION_INFERENCE_PIPELINE
        prompt = prompt.replace("{{ddl_sql}}", self.ddl_sql)
        prompt = prompt.replace("{{data_sql}}", self.data_sql)
        prompt = prompt.replace("{{query_samples_size}}", str(query_samples_needed))
        return prompt

    def _parse_response_content(self, content: str) -> List[QueryRecord]:
        """Parse the response content into a list of QueryRecords."""
        if content.startswith("```json") or content.startswith("```"):
            content = content.split("\n", 1)[1]  # Remove ```json
        if content.endswith("```"):
            content = content.rsplit("\n", 1)[0]  # Remove ```

        try:
            structured_response = QueryRecordResponseFormat.model_validate_json(content)
            return structured_response.items
        except Exception as e:
            raise QueryParsingError(f"Failed to parse response: {e!s}")

    def _validate_query(self, query_record: QueryRecord) -> bool:
        """Verify whether the query is executable."""
        try:
            self.database_manager.select(query_record.sql)
            return True
        except SQLExecutionError as e:
            logger.error(f"{Fore.RED}SQLExecutionError{Fore.RESET}: {e.sql} {e.error_message}")
            return False
        except Exception as e:
            logger.error(
                f"An error occurred while executing the query: "
                f"{query_record.question} {query_record.sql} {e!s}"
            )
            return False

    @timing
    def generate(self, query_samples_size: int = 20) -> SchemaParseResponse:
        """Data generation for samples"""

        dataset: List[QueryRecord] = []
        usage: Optional[dict] = None
        error_query_records: List[QueryRecord] = []

        while len(dataset) < query_samples_size:
            try:
                # Calculate the number of samples to be generated this time.
                samples_needed = query_samples_size - len(dataset)
                prompt = self._prepare_prompt(samples_needed)

                response = self.question_agent.step(
                    prompt, response_format=QueryRecordResponseFormat
                )
                if response.info and 'usage' in response.info:
                    usage = response.info['usage']
                content = response.msgs[0].content.strip()

                # Analyze response content
                query_records = self._parse_response_content(content)

                # Validate and collect valid queries.
                for item in query_records:
                    if self._validate_query(item):
                        dataset.append(item)
                        logger.info(
                            f"Sample collection progress: "
                            f"{Fore.GREEN}{len(dataset)}/{query_samples_size}{Fore.RESET}"
                        )
                    else:
                        error_query_records.append(item)

                # If there are multiple consecutive instances without valid
                # samples, consider redesigning the prompt or exiting early.

            except QueryParsingError as e:
                logger.error(f"Failed to parse response: {e!s}")
            except Exception as e:
                logger.error(f"An unexpected error occurred while generating the sample: {e!s}")

        return SchemaParseResponse(
            data=dataset[:query_samples_size],
            usage=usage,
            errors=error_query_records if error_query_records else None,
        )
