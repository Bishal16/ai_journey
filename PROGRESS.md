# Progress Log — ai_journey

> Running status of the 12-week journey. Update this at the end of each working session so any AI session / any PC can pick up seamlessly. See `ai_backend_engineer_12week_plan.md` for the full roadmap and `CLAUDE.md` for working rules.

**Last updated:** 2026-07-24
**Current week:** Week 5 — Tool calling (give the LLM hands)
**Primary machine:** Mac M3 (also Ubuntu; sync via GitHub)
**LLM provider:** Groq (free tier), model `llama-3.3-70b-versatile`

---

## Environment / setup facts
- Python 3.14.2
- Project root: `ai-backend-portfolio/` (one folder per week)
- venv lives in each week's folder (gitignored). Recreate with `pip install -r requirements.txt`.
- `.env` holds `GROQ_API_KEY=gsk_...` — **gitignored, recreate manually per machine.**

---

## Week 1 — `week01-llm-api` ✅ DONE
FastAPI + Groq `/chat` endpoint. Dockerized. Committed.

## Week 2 — `week01-llm-api` (extended) ✅ DONE
Redis-backed session memory added to `/chat`. Committed.

## Week 3 — `week03-embedding-cli` ✅ DONE
CLI tool: loads .txt files → chunks → embeds with sentence-transformers → stores in ChromaDB → semantic search by query. Committed.

## Week 4 — `week04-rag-api` ✅ DONE
Full RAG API: `POST /upload` (PDF → chunks → embeddings → ChromaDB), `POST /ask` (question → embed → retrieve top-3 → Groq prompt → grounded answer). Tested with Postman. Committed and pushed.

---

## Week 5 — `week05-tool-calling` (IN PROGRESS)

**Goal:** Give the LLM "hands" — let it call real APIs. The LLM decides which tool to call, you execute it, feed the result back to the LLM.

**Architecture:**
```
User question
    ↓
Python FastAPI agent (POST /agent)
    ↓ defines tools as JSON schema
Groq LLM (tool-calling loop)
    ↓ LLM returns: "call get_weather(city=Dhaka)"
Python agent executes HTTP call
    → Java Spring Boot: GET /weather/Dhaka
    ← { "city": "Dhaka", "temp": 32, "condition": "Humid" }
    ↓ feed result back to LLM
Groq LLM synthesizes final answer
    ↓
Response to user
```

**Two services:**
1. `tool-server/` — Java Spring Boot, mocked `GET /weather/{city}` and `GET /currency/convert`
2. `agent/` — Python FastAPI, registers tools + runs the tool-use loop with Groq

**Done:**
- [ ] Scaffold Java Spring Boot tool server
- [ ] Add `/weather/{city}` endpoint (mocked)
- [ ] Add `/currency/convert` endpoint (mocked)
- [ ] Scaffold Python agent FastAPI app
- [ ] Define tools as JSON schema dicts
- [ ] Implement tool-use loop (LLM → tool call → result → LLM)
- [ ] Test end-to-end with Postman

**How to run (once built):**
```bash
# Terminal 1 — Java tool server
cd ai-backend-portfolio/week05-tool-calling/tool-server
./mvnw spring-boot:run   # runs on :8080

# Terminal 2 — Python agent
cd ai-backend-portfolio/week05-tool-calling/agent
source venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

---

## Next up
Finish Week 5, then **Week 6 — LangChain research agent** (web search + RAG + calculator tools).
