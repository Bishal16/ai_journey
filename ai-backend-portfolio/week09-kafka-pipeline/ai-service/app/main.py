
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import psycopg2, os, json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Enrichment Service")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_db():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="events_db",
        user="user",
        password="password"
    )

def enrich_event(event: dict) -> dict:
    prompt = f"""Analyze this business event and return ONLY a JSON object with these fields:
- classified_type: one of [normal_purchase, high_value_transfer, suspicious_login, rapid_refund, new_signup, anomalous_activity]
- entities: object with relevant fields extracted (user_id, amount, country, etc.)
- anomaly_score: float between 0.0 and 1.0 (0=normal, 1=highly suspicious)

Rules for anomaly_score:
- amount > 5000: score >= 0.7
- country not in [BD, US, UK, IN, SG]: score += 0.3
- event_type=refund: score += 0.2
- otherwise: score < 0.3

Event: {json.dumps(event)}

Return ONLY the JSON, no explanation."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


class EventRequest(BaseModel):
    event_id: str
    event_type: str
    user_id: str
    amount: float | None
    metadata: dict


@app.post("/enrich")
def enrich(request: EventRequest):
    event = request.model_dump()
    enriched = enrich_event(event)

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO events (event_id, event_type, raw_payload, classified_type, entities, anomaly_score)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (event_id) DO NOTHING
    """, (
        event["event_id"],
        event["event_type"],
        json.dumps(event),
        enriched.get("classified_type"),
        json.dumps(enriched.get("entities", {})),
        enriched.get("anomaly_score", 0.0)
    ))
    db.commit()
    cur.close()
    db.close()

    return {**event, **enriched}


@app.get("/events")
def get_events(limit: int = 20):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT event_id, event_type, classified_type, entities, anomaly_score, processed_at
        FROM events ORDER BY processed_at DESC LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    db.close()
    return [
        {
            "event_id": r[0],
            "event_type": r[1],
            "classified_type": r[2],
            "entities": r[3],
            "anomaly_score": float(r[4]),
            "processed_at": r[5].isoformat() if hasattr(r[5], 'isoformat') else str(r[5])
        }
        for r in rows
    ]


@app.get("/health")
def health():
    return {"status": "ok"}