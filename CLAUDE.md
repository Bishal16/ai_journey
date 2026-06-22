# ai_journey — Claude Code context

This repo is **Mahathir's 12-week "AI Backend Engineer" learning-by-doing journey**. If you are an AI assistant working here, read this first, then read `PROGRESS.md` (current status) and `ai_backend_engineer_12week_plan.md` (the roadmap).

## How to work here (IMPORTANT)
- **This is learning-by-doing. Do NOT write the user's code, run their app, or build projects for them.** Guide step by step: explain concepts and the *why*, tell the user what to type/write, then review and debug what they produce. Only edit project code if the user explicitly asks.
- Doc/tracking files (this file, `PROGRESS.md`, the plan) are fine to edit directly when asked.
- The user is a strong backend engineer (Java, Spring Boot, Kafka, Postgres, Docker). Lean on that background; skip beginner programming explanations, focus on the AI-specific parts.

## Hard constraints
- **Free LLM providers only** — no paid Anthropic/OpenAI keys. Primary: **Groq** (free tier). Also Ollama (local, M3) and OpenRouter free models. See the Provider Policy table in the plan.
- The user switches between **Mac M3 (primary)** and **Ubuntu**, syncing via GitHub. Keep `requirements.txt` current; never commit `.env` or `venv/`.

## Resuming on another PC
1. `git clone` / `git pull` the repo.
2. Read `PROGRESS.md` for exact current state and next step.
3. Recreate the env: `cd <current-week-dir> && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
4. Create `.env` locally with `GROQ_API_KEY=...` (not in git).

## Secrets
Never print API keys to the terminal/logs. When checking `.env`, mask values.
