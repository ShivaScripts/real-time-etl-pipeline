#!/usr/bin/env python3
import json
import logging
import time
from datetime import datetime
from random import choice, randint

from faker import Faker
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Configuration
KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
TOPIC = "logs"
SEND_INTERVAL_SECONDS = 1  # how often to send a log
DURATION_SECONDS = 5       # how long this script runs

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("log-producer")

# Initialize Faker and Kafka producer
fake = Faker()
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    retries=5
)

SERVICES = ["auth", "payments", "search", "recommendation", "notifications"]
ERROR_CODES = [100, 200, 300, 400, 500]

def generate_log_record() -> dict:
    """Generate a fake, enriched log record."""
    level = choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    record = {
        "event_id": fake.uuid4(),
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "service": choice(SERVICES),
        "message": fake.sentence(nb_words=randint(6, 12)),
        "user_id": fake.uuid4(),
        # add extra fields for transformations
        "response_time_ms": randint(10, 2000),
        "error_code": choice(ERROR_CODES) if level in ("ERROR", "CRITICAL") else None,
        "payload_size_kb": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True) * 10, 2)
    }
    return record

def send_record(record: dict):
    """Send one record to Kafka with error handling."""
    future = producer.send(TOPIC, record)
    try:
        meta = future.get(timeout=10)
        logger.info(f"Sent {record['event_id']} → partition {meta.partition}@offset {meta.offset}")
    except KafkaError as err:
        logger.error(f"Failed to send record: {err}")

def main():
    logger.info("Starting log producer for %s seconds", DURATION_SECONDS)
    start = time.time()
    try:
        while time.time() - start < DURATION_SECONDS:
            rec = generate_log_record()
            send_record(rec)
            time.sleep(SEND_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    finally:
        producer.flush()
        producer.close()
        logger.info("Producer shut down.")

if __name__ == "__main__":
    main()
