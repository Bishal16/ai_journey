from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LLM Chat API")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    model: str

@app.get("/health")
def health():
    return {"status": "ok"}
# Why: A trivial "am I alive?" check — used by Docker/load balancers later. Good first endpoint to confirm the server runs before
# involving the LLM.

# Block 5 — the chat endpoint (the heart of Week 1)

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": request.message}
        ]
    )

    return ChatResponse(
        reply=response.choices[0].message.content,
        model=response.model
    )