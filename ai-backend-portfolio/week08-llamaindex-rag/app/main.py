from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LlamaIndex RAG API")

Settings.llm = Groq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

tech_docs = []
faq_docs = []


@app.get("/health")
def health():
    return {"status": "ok", "tech_docs": len(tech_docs), "faq_docs": len(faq_docs)}


@app.post("/upload/tech")
async def upload_tech(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    tech_docs.append(Document(text=content, metadata={"source": file.filename, "type": "tech"}))
    return {"filename": file.filename, "total_tech_docs": len(tech_docs)}


@app.post("/upload/faq")
async def upload_faq(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8", errors="ignore")
    faq_docs.append(Document(text=content, metadata={"source": file.filename, "type": "faq"}))
    return {"filename": file.filename, "total_faq_docs": len(faq_docs)}


class AskRequest(BaseModel):
    question: str


@app.post("/ask")
def ask(request: AskRequest):
    if not tech_docs and not faq_docs:
        raise HTTPException(status_code=400, detail="No documents uploaded yet.")

    active_tools = []

    if tech_docs:
        tech_index = VectorStoreIndex.from_documents(tech_docs)
        active_tools.append(QueryEngineTool.from_defaults(
            query_engine=tech_index.as_query_engine(),
            description="Useful for answering questions about API rate limits, authentication, endpoints, technical specifications and system documentation"
        ))

    if faq_docs:
        faq_index = VectorStoreIndex.from_documents(faq_docs)
        active_tools.append(QueryEngineTool.from_defaults(
            query_engine=faq_index.as_query_engine(),
            description="Useful for answering questions about passwords, payments, subscriptions, billing, account management and general customer support"
        ))

    if len(active_tools) == 1:
        result = active_tools[0].query_engine.query(request.question)
    else:
        router = RouterQueryEngine(
            selector=LLMSingleSelector.from_defaults(),
            query_engine_tools=active_tools
        )
        result = router.query(request.question)

    return {"answer": str(result)}