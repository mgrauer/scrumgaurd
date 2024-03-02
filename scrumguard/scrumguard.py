import json
import logging
import os
import sys
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, set_global_handler
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.storage.storage_context import StorageContext

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
set_global_handler("simple")


def load_documents():
    reader = SimpleDirectoryReader(input_dir=os.getenv("INGEST_STORAGE_PATH"))
    return reader.load_data()


def load_queries():
    with open(os.getenv("QUERIES_PATH")) as file:
        data = json.load(file)
    return data["queries"]


class VectorStoreManager:
    def __init__(self):
        self.vector_storage_path = os.getenv("VECTOR_STORAGE_PATH")
        logging.info("VectorStoreManager.init: %s", self.vector_storage_path)

    def create_vector_store_from_documents(self, documents):
        vector_index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True,
        )
        vector_index.storage_context.persist(persist_dir=self.vector_storage_path)
        return vector_index

    def create_vector_store_from_index(self):
        if not any(item for item in Path(self.vector_storage_path).iterdir()):
            logging.error("No vector store found at %s", self.vector_storage_path)
            return None

        storage_context = StorageContext.from_defaults(
            persist_dir=self.vector_storage_path
        )
        vector_index = load_index_from_storage(storage_context)
        return vector_index


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Index and RAG local documents.")
    parser.add_argument("--index", action="store_true", help="Index your documents")
    parser.add_argument("--query", action="store_true", help="Query your documents")
    args = parser.parse_args()

    if args.index:
        print("Indexing...")
        documents = load_documents()
        vector_store_manager = VectorStoreManager()
        vector_index = vector_store_manager.create_vector_store_from_documents(
            documents
        )

    if args.query:
        print("Querying...")
        queries = load_queries()
        vector_store_manager = VectorStoreManager()
        vector_index = vector_store_manager.create_vector_store_from_index()
        query_engine = vector_index.as_query_engine(similarity_top_k=2)
        for query in queries:
            response = query_engine.query(query)
            print(response)
