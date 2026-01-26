from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

try:
    print("Initializing embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    print("Embedding query...")
    vec = embeddings.embed_query("Hello world")
    print(f"Success! Vector length: {len(vec)}")
    
    print("Embedding documents...")
    vecs = embeddings.embed_documents(["Hello world", "Another doc"])
    print(f"Success! Embedded {len(vecs)} documents.")

except Exception:
    traceback.print_exc()
