from fastapi import APIRouter, UploadFile, File, HTTPException
from services.parser import DocumentParser
from services.chunker import TextChunker
from services.vector_store import VectorStoreService

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        # 1. Parse Document
        text = DocumentParser.parse_file(content, file.filename)
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from file.")
            
        # 2. Chunk Text
        chunker = TextChunker()
        chunks = chunker.split_text(text)
        
        # 3. Store in Vector DB
        vector_service = VectorStoreService()
        vector_service.create_vector_store(chunks)
        
        return {"message": "Resume uploaded and processed successfully", "chunks_count": len(chunks)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
