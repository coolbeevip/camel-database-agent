from typing import List, Union

from camel.agents import ChatAgent
from camel.models import BaseModelBackend
from pydantic import BaseModel

from camel_database_agent.database.database_manager import DatabaseManager
from camel_database_agent.database_base import timing


class DDLRecord(BaseModel):
    id: str
    summary: str
    sql: str


class DMLRecord(BaseModel):
    id: str
    summary: str
    sql: str


class QueryRecord(BaseModel):
    id: str
    question: str
    sql: str


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
    def parse_ddl_record(self, text: str) -> List[DDLRecord]:
        """Parsing DDL SQL statements"""
        prompt = (
            "Here are some DDL statements from which you need to "
            "extract table names, field names, data types, default "
            "values, etc., to generate summary information and extract "
            "the SQL statements for each table.\n\n"
        )
        prompt += f"```sql\n{text}```\n"
        prompt += "Please output the summary information and SQL script in JSON format."
        response = self.parsing_agent.step(prompt, response_format=DDLRecordResponseFormat)
        ddl_record_response = DDLRecordResponseFormat.model_validate_json(response.msgs[0].content)
        return ddl_record_response.items

    @timing
    def parse_dml_record(self, text: str) -> List[DMLRecord]:
        """Parsing DML SQL statements"""
        prompt = (
            "The following are some DML statements from which you need "
            "to extract table names, field names, and generate summary "
            "information, as well as extract each SQL statement.\n\n"
        )
        prompt += f"```sql\n{text}```\n"
        prompt += "Please output the summary information and SQL script in JSON format."
        response = self.parsing_agent.step(prompt, response_format=DMLRecordResponseFormat)
        dml_record_response = DMLRecordResponseFormat.model_validate_json(response.msgs[0].content)
        return dml_record_response.items

    @timing
    def parse_query_record(self, text: str) -> List[QueryRecord]:
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
        return query_record_response.items
