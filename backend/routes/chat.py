from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag import RAGService

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat_with_resume(request: ChatRequest):
    try:
        if not request.question:
            raise HTTPException(status_code=400, detail="Question is required")
            
        rag_service = RAGService()
        answer = rag_service.ask(request.question)
        
        return {"answer": answer}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
