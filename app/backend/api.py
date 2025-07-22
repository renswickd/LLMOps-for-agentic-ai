from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from app.core.agent import get_response_from_ai_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="LLMOps for Agentic AI")

class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search: bool

@app.post("/chat")
def chat_endpoint(request:RequestState):
    try:
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )
        return {"response" : response}
    
    except Exception as e:
        raise HTTPException(
            status_code=500 , 
            detail=str(CustomException("Failed to get AI response" , error_detail=e))
            )