from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scorer import ScorerService

router = APIRouter()

class AnalyzeRequest(BaseModel):
    job_description: str

@router.post("/analyze")
async def analyze_candidate(request: AnalyzeRequest):
    try:
        if not request.job_description:
            raise HTTPException(status_code=400, detail="Job description is required")
            
        scorer = ScorerService()
        result = scorer.assess_candidate(request.job_description)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
