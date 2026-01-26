from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

class EmbeddingService:
    def __init__(self):
        # Ensure GOOGLE_API_KEY is set in environment variables
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
             print("WARNING: GOOGLE_API_KEY not found in environment.")
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004"
        )

    def get_embedding_function(self):
        return self.embeddings
