import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError, NoBrokersAvailable

from app.schemas.event_schemas import (EventFullyJoinedSchema, EventGetSchema,
                                       EventPostSchema)
from app.services.event_service import EventService
from app.services.priority_service import PriorityService
from app.services.status_service import StatusService
from app.services.system_service import SystemService
from app.services.user_service import UserService
from app.utils import repository_transaction_managaer
from app.utils.logger import log
from app.ws.websocket_manager import websocket_manager
from settings import config


def deserialize_event(event_bytes):
    event_str = event_bytes.decode('utf-8')
    
    event_dict = json.loads(event_str)

    return event_dict


async def consume_events():
    consumer = AIOKafkaConsumer(
        "test_topic",
        bootstrap_servers=f"{config.KAFKA_SERVICE_URL}:{config.KAFKA_SERVICE_PORT}",
    )
    
    repository_manager = repository_transaction_managaer.SqlAlchemyRepositoryTransactionManagaer()
    systems_mapping = await SystemService.get_title_id_mapping(repository_manager)
    priorities_mapping = await PriorityService.get_title_id_mapping(repository_manager)
    user_mapping = await UserService.get_mail_id_mapping(repository_manager)
    status_mapping = await StatusService.get_title_id_mapping(repository_manager)

    event_service = EventService(repository_manager) 

    if not (systems_mapping and priorities_mapping and user_mapping and status_mapping):
        log.info("Failed to load necessary mappings: systems or priorities or user or statuses are missing.")
        raise RuntimeError("Systems or priorities mapping could not be loaded.")
    
    log.info("Consumer started and listening for messages...")
    await consumer.start()
    try:
        async for msg in consumer:
            event = msg.value
            if event is not None:
                event = deserialize_event(event)
                event_for_insert = EventPostSchema(
                    description=event["description"],
                    system_id=systems_mapping[event["system"]],
                    priority_id=priorities_mapping[event["priority"]]
                )
                event_id: int | None = await event_service.insert(
                    event_for_insert, 
                    user_id=None, 
                    status_id=status_mapping["Новый"],
                    created=event["created"]
                )

                if event_id and not await websocket_manager.is_empty_connections_list():
                    event_get: EventFullyJoinedSchema | None = await event_service.get_event_joined(id=event_id)
                    if event_get is None:
                        continue
                    await websocket_manager.broadcast_event(event_get)


    except NoBrokersAvailable as e:
        log.error(f"Kafka broker not available: {e}")
    except KafkaError as e:
        log.error(f"Kafka error occurred: {e}")
        return False
    except Exception as er:
        log.error(f"Consumer event creating error: {er}")
    finally:
        log.info("Consumer stop")
        await consumer.stop()

