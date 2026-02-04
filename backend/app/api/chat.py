from fastapi import APIRouter
from pydantic import BaseModel
from ..rag import get_retriever

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    retriever = get_retriever()
    reply = retriever.get_answer(request.message)
    return ChatResponse(reply=reply)
