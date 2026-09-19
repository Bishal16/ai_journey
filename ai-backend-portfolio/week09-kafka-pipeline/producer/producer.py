import json
import random
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9093",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    api_version=(0, 10, 2)
)

EVENT_TYPES = ["purchase", "login", "transfer", "refund", "signup"]

def generate_event():
    event_type = random.choice(EVENT_TYPES)
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": f"user_{random.randint(1, 100)}",
        "amount": round(random.uniform(10, 10000), 2) if event_type in ["purchase", "transfer", "refund"] else None,
        "metadata": {
            "ip": f"192.168.{random.randint(0,255)}.{random.randint(0,255)}",
            "country": random.choice(["BD", "US", "UK", "IN", "SG"])
        }
    }

while True:
    event = generate_event()
    producer.send("business-events", value=event)
    print(f"Sent: {event['event_type']} | {event['event_id']}")
    time.sleep(2)