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

import logging
import random
from typing import List, Optional, Union

from camel.embeddings import BaseEmbedding
from camel.models import BaseModelBackend
from camel.storages import QdrantStorage
from qdrant_client.conversions.common_types import CollectionInfo

from camel_database_agent.database.schema import QueryRecord
from camel_database_agent.knowledge.knowledge import DatabaseKnowledge

logger = logging.getLogger(__name__)


class DatabaseKnowledgeQdrant(DatabaseKnowledge):
    def __init__(
        self,
        embedding: BaseEmbedding,
        model: Union[BaseModelBackend, List[BaseModelBackend]],
        path: Optional[str] = None,
    ):
        self.path = path
        try:
            table_storage = QdrantStorage(
                vector_dim=embedding.get_output_dim(),
                collection_name="table_documents",
                path=path if path else ":memory:",
            )
            data_storage = QdrantStorage(
                vector_dim=embedding.get_output_dim(),
                collection_name="data_documents",
                path=path if path else ":memory:",
            )
            query_storage = QdrantStorage(
                vector_dim=embedding.get_output_dim(),
                collection_name="query_documents",
                path=path if path else ":memory:",
            )
        except ValueError as e:
            logger.error(
                "Adjust your embedding model to output vectors with "
                "the same dimensions as the existing collection. "
                "Alternatively, delete the existing collection and "
                "recreate it with your current embedding dimensions "
                "(note: this will result in the loss of all existing "
                "data)."
            )
            raise e
        super().__init__(
            embedding=embedding,
            model=model,
            table_storage=table_storage,
            data_storage=data_storage,
            query_storage=query_storage,
        )

    def clear(self) -> None:
        self.table_storage.clear()
        self.data_storage.clear()
        self.query_storage.clear()

    def get_table_collection_size(self) -> int:
        collection_info: CollectionInfo = self.table_storage.client.get_collection(
            "table_documents"
        )
        return collection_info.points_count if collection_info.points_count else 0

    def get_data_collection_size(self) -> int:
        collection_info: CollectionInfo = self.data_storage.client.get_collection("data_documents")
        return collection_info.points_count if collection_info.points_count else 0

    def get_query_collection_size(self) -> int:
        collection_info: CollectionInfo = self.query_storage.client.get_collection(
            "query_documents"
        )
        return collection_info.points_count if collection_info.points_count else 0

    def get_query_collection_sample(self, n: int = 20) -> List[QueryRecord]:
        # Get actual point IDs from the collection
        collection_info = self.query_storage.client.scroll(
            collection_name="query_documents",
            limit=self.get_query_collection_size(),
        )
        point_ids = [point.id for point in collection_info[0]]

        # Sample n random IDs from actual IDs
        random_ids = random.sample(point_ids, min(n, len(point_ids)))

        # Retrieve points using correct IDs
        search_result = self.query_storage.client.retrieve("query_documents", ids=random_ids)
        return [QueryRecord(**record.payload) for record in search_result]
