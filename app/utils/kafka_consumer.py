import json

from kafka import KafkaConsumer
from settings import config

from app.utils.logger import log


def consume_events():
    consumer = KafkaConsumer(
        "test_topic",
        bootstrap_servers=[f"{config.KAFKA_SERVICE_URL}:{config.KAFKA_SERVICE_PORT}"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    log.info("Consumer started and listening for messages...")
    for message in consumer:
        event = message.value
        log.info(event)