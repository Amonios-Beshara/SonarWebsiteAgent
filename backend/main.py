# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent import create_livekit_token, handle_transcript_to_faq
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

# POST /create-session
class CreateSessionRequest(BaseModel):
    company: str

@app.post("/create-session")
async def create_session(data: CreateSessionRequest):
    room_name = f"{data.company}_session"
    token = create_livekit_token(room_name)
    return {
        "room_name": room_name,
        "token": token,
        "livekit_url": os.getenv("LIVEKIT_URL")
    }

# POST /generate-faq
class FAQRequest(BaseModel):
    transcript: str

@app.post("/generate-faq")
async def generate_faq(data: FAQRequest):
    result = await handle_transcript_to_faq(data.transcript)
    return {"faq": result}
