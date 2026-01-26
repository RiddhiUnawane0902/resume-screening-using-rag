import chromadb
from chromadb.config import Settings
import shutil
import os
from .embeddings import EmbeddingService
from langchain_community.vectorstores import Chroma

DB_PATH = "./data/chroma_db"

class VectorStoreService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.db_path = DB_PATH
        # Initialize client with telemetry disabled to fix "ClientStartEvent" error
        self.client = chromadb.PersistentClient(
            path=DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        
    def clear_collection(self):
        """Clears the existing vector store to start fresh for each analysis."""
        try:
            # Instead of deleting the directory (which causes WinError 32),
            # we delete the collection.
            # We iterate through all collections and delete them or just the default one.
            # Langchain uses "langchain" as the default collection name usually.
            collections = self.client.list_collections()
            for collection in collections:
                self.client.delete_collection(collection.name)
        except Exception as e:
            print(f"Error clearing DB: {e}")
        
    def create_vector_store(self, texts: list[str]):
        """Creates a new vector store from text chunks."""
        self.clear_collection()
        
        # Pass the client to Chroma so it uses our settings (no telemetry)
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding_service.get_embedding_function(),
            client=self.client,
            collection_name="resume_collection" 
        )
        return vectorstore

    def get_retriever(self):
        """Returns a retriever for the existing vector store."""
        # Re-initialize Chroma with the same client
        vectorstore = Chroma(
            client=self.client,
            collection_name="resume_collection",
            embedding_function=self.embedding_service.get_embedding_function()
        )
        # Verify k (number of documents to return)
        return vectorstore.as_retriever(search_kwargs={"k": 4})
