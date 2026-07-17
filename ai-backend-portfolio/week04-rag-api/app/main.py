from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from groq import Groq
from sentence_transformers import SentenceTransformer
import chromadb
import os
import io
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG Document Q&A API")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("documents")

class AskRequest(BaseModel):
    question: str

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks
    
@app.get("/health")
def health():
    return {"status": "ok", "chunks_stored": collection.count()}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()
        collection.add(
            ids=[f"{file.filename}-chunk-{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": file.filename}]
        )

    return {"filename": file.filename, "chunks_ingested": len(chunks)}

@app.post("/ask")
def ask(request: AskRequest):
    if collection.count() == 0:
        raise HTTPException(status_code=400, detail="No documents uploaded yet. Use /upload first.")

    query_embedding = embedding_model.encode(request.question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    context_chunks = results["documents"][0]
    sources = list(set(m["source"] for m in results["metadatas"][0]))
    context = "\n\n".join(context_chunks)

    prompt = f"""You are a helpful assistant. Answer the question below using ONLY the context provided.
If the answer is not in the context, say "I don't know based on the provided documents."

    Context:     
    {context}

    Question: {request.question}"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }