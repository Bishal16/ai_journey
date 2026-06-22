from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LLM Chat API")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    model: str

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    redis_key = f"session:{request.session_id}"
    print(1,redis_key)

    history_raw = redis_client.get(redis_key)
    print(2,history_raw)

    history = json.loads(history_raw) if history_raw else []
    print(3,history)

    history.append({"role": "user", "content": request.message})
    print(4,history)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=history
    )

    reply_text = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply_text})
    print(5,history)

    redis_client.set(redis_key, json.dumps(history), ex=3600)

    return ChatResponse(
        reply=reply_text,
        model=response.model
    )