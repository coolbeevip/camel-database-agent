# Copyright 2025 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from camel.agents import ChatAgent
from camel.embeddings import BaseEmbedding
from camel.models import BaseModelBackend
from camel.storages import (
    BaseVectorStorage,
    VectorDBQuery,
    VectorDBQueryResult,
    VectorRecord,
)

from camel_database_agent.core.exceptions import KnowledgeException
from camel_database_agent.core.method_lru_cache import method_lru_cache
from camel_database_agent.database.schema import (
    DDLRecord,
    DMLRecord,
    QueryRecord,
)

RecordType = TypeVar("RecordType", DDLRecord, DMLRecord, QueryRecord)
T = TypeVar("T", DDLRecord, DMLRecord, QueryRecord)


class DatabaseKnowledge(ABC, Generic[T]):
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

        # 存储类型与存储介质的映射
        self._storage_map: Dict[Type[RecordType], BaseVectorStorage] = {  # type: ignore[valid-type]
            DDLRecord: self.table_storage,
            DMLRecord: self.data_storage,
            QueryRecord: self.query_storage,
        }

        # 记录类型与嵌入内容字段的映射
        self._embed_field_map: Dict[Type[RecordType], str] = {  # type: ignore[valid-type]
            DDLRecord: "summary",
            DMLRecord: "summary",
            QueryRecord: "question",
        }

    def add(self, records: List[T]) -> None:
        """添加记录到相应存储中"""
        # 按类型分组记录
        grouped_records: Dict[Type[RecordType], List[RecordType]] = {}  # type: ignore[valid-type]
        for record in records:
            record_type = type(record)
            if record_type not in self._storage_map:
                raise KnowledgeException(f"不支持的记录类型: {record_type}")

            if record_type not in grouped_records:
                grouped_records[record_type] = []
            grouped_records[record_type].append(record)

        # 为每种类型创建向量记录并添加到存储中
        for record_type, type_records in grouped_records.items():
            storage = self._storage_map[record_type]
            embed_field = self._embed_field_map[record_type]

            try:
                v_records = [
                    VectorRecord(
                        vector=self.embedding.embed(getattr(record, embed_field)),
                        payload=record.model_dump(),  # type: ignore[attr-defined]
                    )
                    for record in type_records
                ]
                storage.add(v_records)
            except Exception as e:
                raise KnowledgeException(f"添加记录时发生错误: {e!s}")

    @method_lru_cache(maxsize=128)
    def _generic_query(self, query: str, record_type: Type[T], top_k: int = 8) -> List[T]:
        """General query method, supports caching."""
        storage = self._storage_map.get(record_type)
        if not storage:
            raise KnowledgeException(f"未找到记录类型 {record_type.__name__} 的存储")

        try:
            query_vector = self.embedding.embed(query)
            vector_result: List[VectorDBQueryResult] = storage.query(
                VectorDBQuery(query_vector=query_vector, top_k=top_k)
            )

            records = []
            for result in vector_result:
                if result.record.payload is not None:
                    record: T = record_type(**result.record.payload)
                    records.append(record)
            return records
        except Exception as e:
            raise KnowledgeException(f"查询 {record_type.__name__} 时发生错误: {e!s}")

    def query_ddl(self, query: str, top_k: int = 8) -> List[DDLRecord]:
        """查询DDL记录"""
        return self._generic_query(query, DDLRecord, top_k)

    def query_data(self, query: str, top_k: int = 8) -> List[DMLRecord]:
        """查询DML记录"""
        return self._generic_query(query, DMLRecord, top_k)

    def query_query(self, query: str, top_k: int = 8) -> List[QueryRecord]:
        """查询Query记录"""
        return self._generic_query(query, QueryRecord, top_k)

    @abstractmethod
    def clear(self) -> None:
        """清除所有存储数据"""
        raise NotImplementedError

    @abstractmethod
    def get_table_collection_size(self) -> int:
        """获取表集合的大小"""
        raise NotImplementedError

    @abstractmethod
    def get_data_collection_size(self) -> int:
        """获取数据集合的大小"""
        raise NotImplementedError

    @abstractmethod
    def get_query_collection_size(self) -> int:
        """获取查询集合的大小"""
        raise NotImplementedError

    @abstractmethod
    def get_query_collection_sample(self, n: int = 20) -> List[QueryRecord]:
        """获取查询集合的样本"""
        raise NotImplementedError
