# Progress Log — ai_journey

> Running status of the 12-week journey. Update this at the end of each working session so any AI session / any PC can pick up seamlessly. See `ai_backend_engineer_12week_plan.md` for the full roadmap and `CLAUDE.md` for working rules.

**Last updated:** 2026-09-20
**Current week:** Week 10
**Primary machine:** Mac M3 (also Ubuntu; sync via GitHub)
**LLM provider:** Groq (free tier), model `openai/gpt-oss-120b`

---

## Environment / setup facts
- **Use Python 3.11** — Python 3.14 breaks pydantic/langchain type annotations
- Project root: `ai-backend-portfolio/` (one folder per week)
- venv lives in each week's folder (gitignored). Recreate with `pip install -r requirements.txt`.
- `.env` holds `GROQ_API_KEY=gsk_...` — **gitignored, recreate manually per machine.**
- Groq model: `openai/gpt-oss-120b` (llama-3.3-70b-versatile was removed)

---

## Week 1 — `week01-llm-api` ✅ DONE
FastAPI + Groq `/chat` endpoint. Dockerized. Committed.

## Week 2 — `week01-llm-api` (extended) ✅ DONE
Redis-backed session memory added to `/chat`. Committed.

## Week 3 — `week03-embedding-cli` ✅ DONE
CLI tool: loads .txt files → chunks → embeds with sentence-transformers → stores in ChromaDB → semantic search by query. Committed.

## Week 4 — `week04-rag-api` ✅ DONE
Full RAG API: `POST /upload` (PDF → chunks → embeddings → ChromaDB), `POST /ask` (question → embed → retrieve top-3 → Groq prompt → grounded answer). Tested. Committed.

## Week 5 — `week05-tool-calling` ✅ DONE
Manual tool-calling loop. Java Spring Boot tool server (weather + currency endpoints on :8085). Python FastAPI agent defines tools as JSON schema, runs LLM → tool call → result → LLM loop with Groq. Committed.

## Week 6 — `week06-langchain-agent` ✅ DONE
LangChain research agent. `create_tool_calling_agent` + `AgentExecutor`. Tools: Tavily web search + calculator. Requires `TAVILY_API_KEY`. Committed.

## Week 7 — `week07-mcp-server` ✅ DONE
MCP server with FastMCP. 3 fintech tools: `get_account_balance`, `list_transactions`, `calculate_interest`. Registered in Claude Desktop via `claude_desktop_config.json`. Committed.

## Week 8 — `week08-llamaindex-rag` ✅ DONE
LlamaIndex RAG with RouterQueryEngine. Two indexes (tech docs + FAQ). LLMSingleSelector routes questions to correct index. Committed.

## Week 9 — `week09-kafka-pipeline` ✅ DONE
Full AI-powered event pipeline:
- Python producer → Kafka (port 9093) → Java Spring Boot consumer → Python AI enrichment service → PostgreSQL → Next.js dashboard
- AI service classifies events, extracts entities, scores anomalies (0-1) via Groq
- Dashboard polls `/events` every 3s, highlights high-risk events (score ≥ 0.7) in red
- Infrastructure via Docker Compose (Zookeeper on 2182, Kafka on 9093, Postgres on 5432)

**How to run:**
```bash
cd week09-kafka-pipeline
docker compose up -d

# Terminal 1 — producer
cd producer && source venv/bin/activate && python producer.py

# Terminal 2 — AI service
cd ai-service && source venv/bin/activate && uvicorn app.main:app --reload --port 8001

# Terminal 3 — Java consumer
cd consumer && mvn spring-boot:run

# Terminal 4 — dashboard
cd dashboard && npm run dev   # http://localhost:3000
```

---

## Next up
**Week 10** — to be determined.
