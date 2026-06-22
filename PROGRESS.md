# Progress Log — ai_journey

> Running status of the 12-week journey. Update this at the end of each working session so any AI session / any PC can pick up seamlessly. See `ai_backend_engineer_12week_plan.md` for the full roadmap and `CLAUDE.md` for working rules.

**Last updated:** 2026-06-22
**Current week:** Week 1 — Talk to an LLM via API
**Primary machine:** Mac M3 (also Ubuntu; sync via GitHub)
**LLM provider:** Groq (free tier), model `llama-3.3-70b-versatile`

---

## Environment / setup facts
- Python 3.14.2
- Project root: `ai-backend-portfolio/` (one folder per week)
- Week 1 dir: `ai-backend-portfolio/week01-llm-api/`
- venv lives in each week's folder (gitignored). Recreate with `pip install -r requirements.txt`.
- `.env` holds `GROQ_API_KEY=gsk_...` — **gitignored, recreate manually per machine.**

---

## Week 1 — `week01-llm-api`  (IN PROGRESS)
**Goal:** FastAPI service that sends a question to a free LLM and returns the reply. Learn: messages array, roles, tokens, API-key auth, FastAPI/Pydantic models, env vars.

**Done:**
- [x] Project scaffold + venv + structure
- [x] Free provider chosen: **Groq** (key in `.env`, format verified)
- [x] `groq` library installed; `requirements.txt` updated
- [x] `app/main.py` written — `GET /health` + `POST /chat`
- [x] Ran locally (`uvicorn app.main:app --reload`), tested at `/docs`
- [x] **`/chat` returns a real LLM reply** ✅ (core week-1 goal hit)
- [x] Committed locally

**Remaining:**
- [ ] Dockerize (`Dockerfile` already scaffolded, not yet built/tested)
- [ ] Deploy to Oracle Cloud VM (open port 8000 in security list)
- [ ] Create GitHub remote + push
- [ ] Write `week01-llm-api/README.md`
- [ ] (stretch) `POST /chat/stream` — token streaming via SSE
- [ ] (optional learning) test empty-message 400 path; print token usage

**How to run Week 1 locally:**
```bash
cd ai-backend-portfolio/week01-llm-api
source venv/bin/activate          # create first if missing
uvicorn app.main:app --reload     # then open http://localhost:8000/docs
```

---

## Next up
Finish Week 1 remaining items (Docker → deploy → GitHub → README), then start **Week 2 — add Redis-backed conversation memory**.

## Decisions log
- Provider = Groq for Weeks 1–2 (fast, free, OpenAI-compatible, real API-auth practice). Ollama planned for Week 3 embeddings; OpenRouter for Week 5+ model comparison.
