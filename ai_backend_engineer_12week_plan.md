# 🗺️ 12-Week AI Backend Engineer Roadmap
**For:** Mahathir Mohammad Bishal — Backend Engineer → AI Application Engineer  
**Time commitment:** 1–1.5 hrs/weekday, 3–4 hrs/weekend  
**Goal:** Hireable as an AI Application/Backend Engineer building RAG systems, AI agents, LLM-integrated APIs, and MCP servers

---

## 💸 Provider Policy — Free Only

This journey uses **only free LLM providers** (no paid Anthropic/OpenAI keys). Wherever the weeks below say "OpenAI/Anthropic", substitute the free equivalent. The concepts are identical because these are all OpenAI-compatible APIs — only the provider/key changes.

| Need | Free choice | Notes |
|---|---|---|
| **LLM chat/completions** | **Groq** (free tier, no card) — `console.groq.com` | Fast, OpenAI-compatible. Primary provider Weeks 1–2. |
| **Local LLM (offline, no key)** | **Ollama** on the Mac M3 | Free forever; use from Week 3 onward where local models shine. |
| **Model variety / comparison** | **OpenRouter** free models (`:free`) | Reach for in Week 5+ when comparing models for tasks. |
| **Embeddings** | **`sentence-transformers`** (local) or **Ollama** `nomic-embed-text` | Free local embeddings — no paid embedding API. |
| **Web search (agents)** | **Tavily** free tier | Already free in the plan. |

Current LLM model in use: `llama-3.3-70b-versatile` (Groq).

---

## Phase 1 — Foundation (Weeks 1–4): Ship a RAG App

---

### Week 1 — Talk to an LLM via API, wrap it in a REST endpoint

**Project to build:**  
A FastAPI service with two endpoints — `POST /chat` (sends a message to an LLM via Groq's free API, returns response) and `GET /health`. Dockerize it and run it on your Oracle VM.

**Concepts learned through building:**
- LLM API basics (messages array, roles, tokens, max_tokens)
- Python virtual environments, `pip`, project structure
- FastAPI request/response models (familiar concept, new syntax)
- Environment variables for API key management

**Stack:** Python, FastAPI, Groq SDK (free tier), Docker

**Stretch goal:** Add a `POST /chat/stream` endpoint that streams the response token by token using SSE

---

### Week 2 — Add memory: make it a stateful conversation API

**Project to build:**  
Extend Week 1's service. Add Redis to store conversation history per `session_id`. Each `POST /chat` reads history from Redis, appends to the messages array, calls the LLM, stores the response back. Stateful chat over pure HTTP.

**Concepts learned through building:**
- Context window — why history management matters
- System prompts — how to shape model behavior
- Redis as a session store (you already know Redis, this clicks fast)
- Token counting — why you can't store infinite history

**Stack:** Python, FastAPI, Redis, Docker Compose

**Stretch goal:** Implement a sliding window — automatically drop oldest messages when token count exceeds a threshold

---

### Week 3 — Embeddings and vector search

**Project to build:**  
A CLI tool that takes a folder of `.txt` or `.md` files, chunks them, generates embeddings via a **free local** embedding model, and stores them in **ChromaDB** (local). Then accepts a query, embeds it, and returns the top 3 most semantically similar chunks.

**Concepts learned through building:**
- What embeddings are (vectors that capture meaning)
- Chunking strategies — fixed size vs sentence boundary
- Cosine similarity — what "nearest neighbor" means
- ChromaDB collections, `add()`, `query()`

**Stack:** Python, ChromaDB, `sentence-transformers` (free local embeddings) or Ollama `nomic-embed-text`

**Stretch goal:** Add metadata filtering — store document source as metadata, allow querying only within a specific file

---

### Week 4 — Full RAG app, deployed

**Project to build:**  
Combine Weeks 1–3. Build a **document Q&A API** — user uploads a PDF via `POST /upload`, it gets chunked and embedded into ChromaDB. `POST /ask` takes a question, retrieves top-k relevant chunks, injects them into the LLM prompt as context, returns a grounded answer. Deploy on your Oracle VM with Docker Compose (FastAPI + ChromaDB + Redis).

**Concepts learned through building:**
- The RAG pipeline end-to-end: ingest → embed → retrieve → augment → generate
- Prompt construction with retrieved context
- Why RAG beats fine-tuning for most use cases
- Basic eval: does the answer actually use the context?

**Stack:** Python, FastAPI, ChromaDB, Groq (free LLM API), Docker Compose, Linux

**Stretch goal:** Add a `/sources` field in the response that cites which document chunks were used to generate the answer

---

## Phase 2 — Agents & Tooling (Weeks 5–8)

---

### Week 5 — Tool calling: give the LLM hands

**Project to build:**  
A **Java Spring Boot API** that exposes two endpoints — `GET /weather/{city}` (mocked) and `GET /currency/convert`. Build a Python FastAPI layer that registers these as LLM tools. User asks *"What's the weather in Dhaka and convert 100 USD to BDT?"* — the LLM decides which tools to call, calls them via HTTP, synthesizes the answer.

**Concepts learned through building:**
- Tool/function calling spec (JSON schema definitions)
- The tool-use loop: LLM → tool call → result → LLM again
- How your existing Java APIs become AI-callable tools
- Parallel tool calls

**Stack:** Java Spring Boot (tool server), Python FastAPI (agent layer), Groq/OpenRouter free tool-calling API

**Stretch goal:** Add a `GET /stock/{symbol}` tool and handle cases where the LLM calls a tool with invalid parameters — return a graceful error back into the loop

---

### Week 6 — LangChain: build a multi-step research agent

**Project to build:**  
A **research assistant agent** using LangChain. Give it three tools: web search (Tavily API — free tier), your ChromaDB RAG from Week 4, and a calculator tool. User asks a complex question — agent plans, searches, retrieves, computes, then writes a structured answer. Expose it via FastAPI.

**Concepts learned through building:**
- LangChain `AgentExecutor`, `create_tool_calling_agent`
- Chain composition — how steps pipe into each other
- LangChain vs raw API calls — when the abstraction helps
- Intermediate reasoning steps (chain of thought in action)

**Stack:** Python, LangChain, Tavily Search API, ChromaDB, FastAPI

**Stretch goal:** Add `LangSmith` tracing (free tier) so you can see the full agent reasoning trace in a UI — invaluable for debugging

---

### Week 7 — MCP server: your Java backend as an AI tool provider

**Project to build:**  
Build an **MCP server in Python** (using the `mcp` SDK) that exposes tools from your existing domain knowledge — e.g. a fintech-themed MCP server with tools like `get_account_balance`, `list_transactions`, `calculate_interest`. Connect it to Claude Desktop and query it conversationally. Then write a blog post or README explaining what MCP is.

**Concepts learned through building:**
- MCP protocol — tools, resources, prompts primitives
- How MCP differs from raw tool calling (standardization, discoverability)
- Building an MCP server with the Python SDK
- Why MCP matters for enterprise AI integration (your resume story)

**Stack:** Python, `mcp` SDK, Claude Desktop for testing

**Stretch goal:** Port the MCP server to call your real Java Spring Boot API under the hood — now Claude can talk to your Java backend through MCP

---

### Week 8 — LlamaIndex: production RAG with proper indexing

**Project to build:**  
Rebuild your Week 4 RAG using **LlamaIndex** instead of raw ChromaDB. Use `VectorStoreIndex`, add a `RouterQueryEngine` that routes questions to different indexes (e.g. one for technical docs, one for FAQs). Compare retrieval quality against your Week 4 version.

**Concepts learned through building:**
- LlamaIndex abstractions vs LangChain — when to use which
- Query routing — multi-index RAG
- Reranking — using a cross-encoder to improve retrieval precision
- Persistent storage for indexes

**Stack:** Python, LlamaIndex, ChromaDB or Qdrant, FastAPI

**Stretch goal:** Add `HyDE` (Hypothetical Document Embeddings) — generate a hypothetical answer first, embed that for retrieval instead of the raw question. Noticeably improves results.

---

## Phase 3 — Capstone (Weeks 9–12): Portfolio Project

---

### Week 9 — Design & scaffold the capstone

**Project:**  
**AI-Powered Event Processing Backend** — an intelligent Kafka consumer that processes business events (e.g. transaction events, order events), enriches them using an LLM, classifies them, flags anomalies, and stores structured results. Think: your MemLedger/VoIP background meets AI.

This week: design the architecture, scaffold all services, write the README with architecture diagram.

**Architecture:**
```
Kafka Topic (raw events)
    ↓
Java Spring Boot Consumer (your strength)
    ↓
Python AI Enrichment Service (FastAPI)
  - Classifies event type
  - Extracts entities via LLM
  - Flags anomalies via prompt
    ↓
PostgreSQL (structured results)
    ↓
REST API to query results
```

**Concepts learned:** System design for AI-integrated backends, async AI enrichment patterns, separating AI layer from core backend

**Stack:** Java Spring Boot, Python FastAPI, Kafka, PostgreSQL, Docker Compose

---

### Week 10 — Build the AI enrichment service

**Project to build:**  
Build the Python FastAPI enrichment service. It receives a raw event JSON, runs it through a structured LLM call (using JSON mode / structured output), returns: `event_category`, `entities_extracted`, `anomaly_score` (0–1), `anomaly_reason`. Write tests with mocked LLM responses.

**Concepts learned through building:**
- Structured outputs / JSON mode — get reliable JSON from LLMs
- Prompt design for classification tasks
- Latency budgeting — LLM calls are slow, how do you not block Kafka?
- Testing AI services — mocking LLM responses

**Stack:** Python, FastAPI, Pydantic, Groq/OpenRouter structured output (free), pytest

**Stretch goal:** Add a fallback — if the LLM call fails or times out, use a simple rule-based classifier so the pipeline never stalls

---

### Week 11 — Wire everything together + RAG for anomaly context

**Project to build:**  
Wire the full pipeline. Java consumer reads from Kafka → calls Python enrichment service → stores to PostgreSQL. Add a RAG component: a knowledge base of known fraud patterns and business rules. Enrichment service retrieves relevant rules before classifying — grounded anomaly detection.

**Concepts learned through building:**
- End-to-end async AI pipeline
- RAG as a knowledge injection layer (not just Q&A)
- Idempotency in AI pipelines — what if enrichment is called twice?
- Observability — log LLM inputs/outputs for debugging

**Stack:** Full stack from Week 9 + ChromaDB/Qdrant for rules knowledge base

---

### Week 12 — Polish, deploy, document

**Project:**  
Deploy the full stack on your Oracle VM. Write a production-quality README with architecture diagram (use `draw.io` or Excalidraw), setup instructions, and example API calls. Record a 3-minute Loom demo. Publish to GitHub.

**Checklist:**
- [ ] Docker Compose for the full stack (one command to run everything)
- [ ] `.env.example` with all required variables
- [ ] Architecture diagram
- [ ] README with problem statement, solution, and tech decisions
- [ ] Loom walkthrough video linked in README

---

## 📄 Resume Bullets — Copy These After Week 12

**Add a new "AI Engineering" section:**

```
Built end-to-end RAG pipeline using Python, LangChain, and ChromaDB —
document ingestion, embedding, semantic retrieval, and LLM-augmented
response generation, deployed on Linux with Docker

Architected an AI-powered Kafka event enrichment pipeline integrating
Java Spring Boot consumers with a Python FastAPI LLM enrichment service —
structured entity extraction, anomaly classification, and RAG-grounded
fraud pattern detection

Built MCP (Model Context Protocol) server exposing domain business logic
as AI-callable tools, enabling LLM clients to interact with backend APIs
through the standardized MCP protocol

Developed multi-tool LangChain agent with web search, vector retrieval,
and external API tool calling — exposed via FastAPI with full LangSmith
observability tracing
```

**Add to Technical Skills:**

```
AI/LLM: LangChain, LlamaIndex, RAG, Vector Databases (ChromaDB, Qdrant),
LLM APIs (Groq, OpenRouter, Ollama), Tool Calling, AI Agents, MCP,
Prompt Engineering, FastAPI
```

---

## 📁 GitHub Structure

Make a pinned repo called **`ai-backend-portfolio`** with this structure:

```
ai-backend-portfolio/
├── week01-llm-api/
├── week02-stateful-chat/
├── week03-embeddings-cli/
├── week04-rag-api/              ← deployed, link in README
├── week05-tool-calling/
├── week06-langchain-agent/
├── week07-mcp-server/           ← this one gets attention
├── week08-llamaindex-rag/
└── capstone-ai-event-pipeline/  ← your hero project
    ├── README.md (with architecture diagram + Loom link)
    ├── docker-compose.yml
    └── services/
```

Each subfolder needs its own short README — what it does, how to run it, what you learned. Recruiters skim GitHub. Make each one self-explanatory in 30 seconds.

---

> **Note:** The MCP server (Week 7) and the Kafka+AI capstone are your two most differentiating projects — they directly connect your existing backend credibility to AI, which almost no fresher AI engineer can claim.
![]()