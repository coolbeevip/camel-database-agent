from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Union

from camel.agents import ChatAgent
from camel.embeddings import BaseEmbedding
from camel.models import BaseModelBackend
from camel.storages import (
    BaseVectorStorage,
    VectorDBQuery,
    VectorDBQueryResult,
    VectorRecord,
)

from camel_database_agent.database.database_schema_parse import (
    DDLRecord,
    DMLRecord,
    QueryRecord,
)

RecordType = TypeVar("RecordType", DDLRecord, DMLRecord, QueryRecord)


class DatabaseKnowledge(ABC):
    def __init__(
        self,
        embedding: BaseEmbedding,
        model: Union[BaseModelBackend, List[BaseModelBackend]],
        table_storage: BaseVectorStorage,
        data_storage: BaseVectorStorage,
        query_storage: BaseVectorStorage,
        **data: Any,
    ):
        super().__init__(**data)
        self.embedding = embedding
        self.table_storage = table_storage
        self.data_storage = data_storage
        self.query_storage = query_storage
        self.ddl_parsing_agent = ChatAgent(
            system_message="You are a database expert, skilled at parsing "
            "DDL statements, extracting key information, and "
            "converting it into JSON format.",
            model=model,
            message_window_size=10,
        )

    def add(self, records: List[RecordType]) -> None:
        ddl_records: List[DDLRecord] = []
        dml_records: List[DMLRecord] = []
        query_records: List[QueryRecord] = []
        for record in records:
            if isinstance(record, DDLRecord):
                ddl_records.append(record)
            elif isinstance(record, DMLRecord):
                dml_records.append(record)
            elif isinstance(record, QueryRecord):
                query_records.append(record)
            else:
                raise ValueError(f"Unknown record type: {record}")

        if len(ddl_records) > 0:
            v_records = [
                VectorRecord(
                    vector=self.embedding.embed(record.summary),
                    payload=record.model_dump(),
                )
                for record in ddl_records
            ]
            self.table_storage.add(v_records)
        if len(dml_records) > 0:
            v_records = [
                VectorRecord(
                    vector=self.embedding.embed(record.summary),
                    payload=record.model_dump(),
                )
                for record in dml_records
            ]
            self.data_storage.add(v_records)
        if len(query_records) > 0:
            v_records = [
                VectorRecord(
                    vector=self.embedding.embed(record.question),
                    payload=record.model_dump(),
                )
                for record in query_records
            ]
            self.query_storage.add(v_records)

    def query_ddl(self, query: str, top_k: int = 8) -> List[DDLRecord]:
        if self.table_storage:
            records = []
            query_vector = self.embedding.embed(query)
            vector_result: List[VectorDBQueryResult] = self.table_storage.query(
                VectorDBQuery(query_vector=query_vector, top_k=top_k)
            )
            for result in vector_result:
                if result.record.payload is not None:
                    records.append(DDLRecord(**result.record.payload))
            return records
        else:
            raise ValueError("Table storage is not set")

    def query_data(self, query: str, top_k: int = 8) -> List[DMLRecord]:
        if self.data_storage:
            records = []
            query_vector = self.embedding.embed(query)
            vector_result: List[VectorDBQueryResult] = self.data_storage.query(
                VectorDBQuery(query_vector=query_vector, top_k=top_k)
            )
            for result in vector_result:
                if result.record.payload is not None:
                    records.append(DMLRecord(**result.record.payload))
            return records
        else:
            raise ValueError("Data storage is not set")

    def query_query(self, query: str, top_k: int = 8) -> List[QueryRecord]:
        if self.query_storage:
            records = []
            query_vector = self.embedding.embed(query)
            vector_result: List[VectorDBQueryResult] = self.query_storage.query(
                VectorDBQuery(query_vector=query_vector, top_k=top_k)
            )
            for result in vector_result:
                if result.record.payload is not None:
                    records.append(QueryRecord(**result.record.payload))
            return records
        else:
            raise ValueError("Query storage is not set")

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_table_collection_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_data_collection_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_query_collection_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_query_collection_sample(self, n: int = 20) -> List[QueryRecord]:
        raise NotImplementedError
