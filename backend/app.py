#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.rag import generate_answer

app = FastAPI(title="AI Supplement Advisor")

# -------------------------
# CORS CONFIG (VERY IMPORTANT)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# REQUEST MODEL
# -------------------------
class AskRequest(BaseModel):
    question: str

# -------------------------
# API ENDPOINT
# -------------------------
@app.post("/ask")
def ask(data: AskRequest):
    answer = generate_answer(data.question)
    return {"answer": answer}
