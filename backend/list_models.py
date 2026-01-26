import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    # Try to load from main.py check or just assume it's in env
    print("No API Key found in env")
else:
    genai.configure(api_key=api_key)
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Generative Model: {m.name}")
        if 'embedContent' in m.supported_generation_methods:
            print(f"Embedding Model: {m.name}")
