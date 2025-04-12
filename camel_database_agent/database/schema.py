import textwrap
from typing import Generic, List, Optional, TypeVar, Union

from camel.agents import ChatAgent
from camel.models import BaseModelBackend
from pydantic import BaseModel

from camel_database_agent.database.manager import DatabaseManager
from camel_database_agent.database_base import timing


class DDLRecord(BaseModel):
    id: str
    summary: str
    sql: str


class DMLRecord(BaseModel):
    id: str
    summary: str
    dataset: str


class QueryRecord(BaseModel):
    id: str
    question: str
    sql: str


T = TypeVar('T', bound=BaseModel)


class SchemaParseResponse(BaseModel, Generic[T]):
    data: List[T]
    usage: Optional[dict]
    errors: Optional[List[T]] = None


class DDLRecordResponseFormat(BaseModel):
    items: List[DDLRecord]


class DMLRecordResponseFormat(BaseModel):
    items: List[DMLRecord]


class QueryRecordResponseFormat(BaseModel):
    items: List[QueryRecord]


class DatabaseSchemaParse:
    def __init__(
        self,
        database_manager: DatabaseManager,
        model: Union[BaseModelBackend, List[BaseModelBackend]],
    ):
        self.database_manager = database_manager
        self.parsing_agent = ChatAgent(
            system_message="You are a database expert, proficient in the "
            "SQL syntax of various databases.",
            model=model,
        )

    @timing
    def parse_ddl_record(self, text: str) -> SchemaParseResponse:
        """Parsing DDL Schema"""
        prompt = (
            "Translate the following information into a JSON array format, "
            "with each JSON object in the array containing three "
            "elements: "
            "\"id\" for the table name, "
            "\"summary\" for a summary of the table, and "
            "\"sql\" for the SQL statement of the table creation.\n\n"
        )
        if text.startswith("```sql"):
            prompt += f"{text}\n\n"
        else:
            prompt += f"```sql\n{text}```\n\n"

        # 非 openai 模型要增加以下片段
        prompt += textwrap.dedent(
            "Output Format:\n"
            "{"
            "    \"items\":"
            "        ["
            "            {"
            "                \"id\": \"<table name>\","
            "                \"summary\": \"<table summary>\","
            "                \"sql\": \"<table ddl script>\""
            "            }"
            "        ]"
            "}\n\n"
        )
        prompt += "Now, directly output the JSON array without explanation."
        response = self.parsing_agent.step(prompt, response_format=DDLRecordResponseFormat)
        ddl_record_response = DDLRecordResponseFormat.model_validate_json(response.msgs[0].content)
        return SchemaParseResponse(data=ddl_record_response.items, usage=response.info["usage"])

    @timing
    def parse_dml_record(self, text: str) -> SchemaParseResponse:
        """Parsing Sampled Data"""
        prompt = (
            "Translate the following information into a JSON array format, "
            "with each JSON object in the array containing three "
            "elements: "
            "\"id\" for the table name, "
            "\"summary\" for a summary of the table, and "
            "\"dataset\" for the Markdown of the data.\n\n"
        )
        prompt += f"{text}\n\n"

        # 非 openai 模型要增加以下片段
        prompt += textwrap.dedent(
            "Output Format:\n"
            "{"
            "    \"items\":"
            "        ["
            "            {"
            "                \"id\": \"<table name>\","
            "                \"summary\": \"<table summary>\","
            "                \"dataset\": \"<markdown dataset>\""
            "            }"
            "        ]"
            "}\n\n"
        )
        prompt += "Now, directly output the JSON array without explanation."
        response = self.parsing_agent.step(prompt, response_format=DMLRecordResponseFormat)
        dml_record_response = DMLRecordResponseFormat.model_validate_json(response.msgs[0].content)
        return SchemaParseResponse(data=dml_record_response.items, usage=response.info["usage"])

    @timing
    def parse_query_record(self, text: str) -> SchemaParseResponse:
        """Parsing Query SQL statements"""
        prompt = (
            "The following is an analysis of user query requirements, "
            "from which you need to extract user questions and "
            "corresponding SQL statements.\n\n"
        )
        prompt += f"```sql\n{text}```\n"
        prompt += "Please output the summary information and SQL script in JSON format."
        response = self.parsing_agent.step(prompt, response_format=QueryRecordResponseFormat)
        query_record_response = QueryRecordResponseFormat.model_validate_json(
            response.msgs[0].content
        )
        return SchemaParseResponse(data=query_record_response.items, usage=response.info["usage"])
