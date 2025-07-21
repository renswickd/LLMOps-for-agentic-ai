from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

app = FastAPI(title="LLMOps for Agentic AI")

class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search: bool