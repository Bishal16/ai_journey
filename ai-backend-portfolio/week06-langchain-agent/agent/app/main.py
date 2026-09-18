from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LangChain Research Agent")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

search_tool = TavilySearchResults(
    max_results=3,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Input must be a valid Python math expression like '100 / 50 * 3'"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

tools = [search_tool, calculator]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful research assistant. Use the tools available to answer questions thoroughly."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

class ResearchRequest(BaseModel):
    question: str

@app.post("/research")
def research(request: ResearchRequest):
    result = executor.invoke({"input": request.question})
    return {"answer": result["output"]}

@app.get("/health")
def health():
    return {"status": "ok"}
