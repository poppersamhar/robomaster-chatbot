from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat_router

app = FastAPI(title="RoboMaster AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")


@app.get("/health")
async def health_check():
    return {"status": "ok"}
