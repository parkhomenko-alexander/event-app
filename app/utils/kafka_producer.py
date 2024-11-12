import json

from aiokafka import AIOKafkaProducer

from settings import config


def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer configuration
async def create_producer():
    prod = AIOKafkaProducer(
        bootstrap_servers=f"{config.KAFKA_SERVICE_URL}:{int(config.KAFKA_SERVICE_PORT)}",
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )
    await prod.start()
    return prod  