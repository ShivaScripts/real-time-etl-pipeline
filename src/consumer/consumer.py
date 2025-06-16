#!/usr/bin/env python3
import json
import logging
import os
import signal
import sys
from datetime import datetime

from kafka import KafkaConsumer
from kafka.errors import KafkaError

# Configuration
KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
TOPIC = "logs"
OUTPUT_DIR = "data/raw_logs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"logs_{datetime.utcnow().strftime('%Y%m%d')}.jsonl")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("log-consumer")

# Initialize consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="log-consumers",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

def shutdown(signum, frame):
    logger.info("Shutdown signal received. Closing consumer.")
    consumer.close()
    sys.exit(0)

def main():
    # Graceful shutdown on SIGINT/SIGTERM
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info(f"Starting consumer, writing to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "a") as f:
        try:
            for message in consumer:
                record = message.value
                f.write(json.dumps(record) + "\n")
                logger.info(f"Wrote record offset {message.offset}")
        except KafkaError as err:
            logger.error(f"Consumer error: {err}")
        finally:
            consumer.close()

if __name__ == "__main__":
    main()
