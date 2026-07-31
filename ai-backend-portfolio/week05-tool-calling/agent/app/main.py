# Block 1 — imports and setup:
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Tool Calling Agent")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

REST_API_SERVER = "http://localhost:8085"

# Block 2 — tool definitions (JSON schema):
payloads = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert an amount from one currency to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount to convert"},
                    "from_currency": {"type": "string", "description": "Source currency code e.g. USD"},
                    "to_currency": {"type": "string", "description": "Target currency code e.g. BDT"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    }
]


# Block 3 — tool executor:
def execute_tool(name: str, args: dict) -> str:
    if name == "get_weather":
        r = httpx.get(f"{REST_API_SERVER}/weather/{args['city']}")
        return str(r.json())
    elif name == "convert_currency":
        r = httpx.get(f"{REST_API_SERVER}/currency/convert", params={
            "amount": args["amount"],
            "from": args["from_currency"],
            "to": args["to_currency"]
        })
        return str(r.json())
    return "Unknown tool"


# Block 4 — the agent endpoint:
class AgentRequest(BaseModel):
    question: str

@app.post("/agent")
def agent(request: AgentRequest):
    messages = [{"role": "user", "content": request.question}]

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=payloads,
            tool_choice="auto"
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return {"answer": msg.content}

        messages.append(msg)

        for tool_call in msg.tool_calls:
            result = execute_tool(
                tool_call.function.name,
                __import__("json").loads(tool_call.function.arguments)
            )
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

# Block 5 — health:
@app.get("/health")
def health():
    return {"status": "ok"}