from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, analyze, chat
import os
from dotenv import load_dotenv

load_dotenv()
# os.environ["GOOGLE_API_KEY"] = "..."

app = FastAPI(title="Resume Screening & RAG Tool")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(analyze.router, prefix="/api", tags=["Analyze"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "Resume Screening API is running"}
