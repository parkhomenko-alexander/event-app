import json
import time

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

from settings import config


def serializer(message):
    return json.dumps(message).encode('utf-8')



# Producer
def kafka_producer():
    print(config.KAFKA_SERVICE_URL, config.KAFKA_SERVICE_PORT)
    
    producer = KafkaProducer(
        bootstrap_servers=[f"{config.KAFKA_SERVICE_URL}:{int(config.KAFKA_SERVICE_PORT)}"],
        value_serializer=serializer
    )
    
    for i in range(3):
        data = {"number": i}
        producer.send("test_topic", value=data)
        print(f"Sent: {data}")
        time.sleep(1)

    producer.flush()
    producer.close()

if __name__ == "__main__":
    print("Starting Kafka Producer...")
    kafka_producer()
