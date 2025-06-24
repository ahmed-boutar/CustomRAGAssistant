# app/routes/inference.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth import get_current_user
from app.services.query_handler import run_chat
from typing import Optional
from ..database import get_db

router = APIRouter(prefix="/chat", tags=["ChatInference"])

# class ChatInferenceRequest(BaseModel):
#     model: str 
#     user_input: str
#     system_prompt: str = "You are a helpful assistant."
#     chat_history: list = []  # list of {"role": "user"/"assistant", "content": "..."}

class ChatMessageInput(BaseModel):
    role: str
    content: str

class ChatInferenceRequest(BaseModel):
    model: str
    system_prompt: str = "You are a helpful assistant."
    session_id: int
    user_input: str
    enable_rag: Optional[bool] = False

# @router.post("/")
# def chat(request: ChatInferenceRequest, user=Depends(get_current_user)):
#     # TODO: Implement content filtering
#     # if not filter_prompt(request.prompt):
#     #     raise HTTPException(status_code=400, detail="Prompt violates content policy.")
#     try:
#         response = run_chat(
#             model=request.model,
#             system_prompt=request.system_prompt,
#             chat_history=request.chat_history,
#             user_input=request.user_input
#         )
#         return {"response": response}
#     except Exception as e:
#         print(f"Error during chat inference: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def chat(request: ChatInferenceRequest, user=Depends(get_current_user), db=Depends(get_db)):
    try:
        response = run_chat(
            db=db,
            user_id=user.id,
            session_id=request.session_id,
            model=request.model,
            system_prompt=request.system_prompt,
            user_input=request.user_input,
            enable_rag=request.enable_rag,
        )
        return {"response": response}
    except Exception as e:
        print(f"Error during chat inference: {e}")
        raise HTTPException(status_code=500, detail=str(e))
