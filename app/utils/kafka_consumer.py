import json

from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app.exeptions.event_exceptions import EventValidationError
from app.schemas.event_schemas import (EventFullyJoinedSchema, EventPostSchema,
                                       RawEventInfoSchema)
from app.services.event_service import EventService
from app.services.priority_service import PriorityService
from app.services.status_service import StatusService
from app.services.system_service import SystemService
from app.services.user_service import UserService
from app.settings import config
from app.utils import building_cache, repository_transaction_managaer
from app.utils.building_cache import get_building_cache
from app.utils.logger import log
from app.utils.redis_manager import RedisManager
from app.ws.websocket_manager import websocket_manager


def deserialize_event(event_bytes) -> RawEventInfoSchema:
    event_str = event_bytes.decode('utf-8')
    
    event_dict = json.loads(event_str)

    return RawEventInfoSchema(**event_dict)

async def consume_events() -> None:
    consumer = AIOKafkaConsumer(
        config.KAFKA_TOPIC_NAME_EVENTS,
        bootstrap_servers=f"{config.KAFKA_SERVICE_URL}:{config.KAFKA_SERVICE_PORT}",
    )
    
    repository_manager = repository_transaction_managaer.SqlAlchemyRepositoryTransactionManagaer()
    systems_mapping = await SystemService.get_title_id_mapping(repository_manager)
    priorities_mapping = await PriorityService.get_title_id_mapping(repository_manager)
    user_mapping = await UserService.get_mail_id_mapping(repository_manager)
    status_mapping = await StatusService.get_title_id_mapping(repository_manager)

    event_service = EventService(repository_manager, get_building_cache())
    if not (systems_mapping and priorities_mapping and user_mapping and status_mapping):
        log.info("Failed to load necessary mappings: systems, priorities, user, or statuses are missing.")
        raise RuntimeError("Systems or priorities mapping could not be loaded.")

    try:
        await consumer.start()
        log.info("Consumer started and listening for messages...")

        async for msg in consumer:
            event = msg.value
            if event is not None:
                dser_event: RawEventInfoSchema = deserialize_event(event)
                

                event_for_insert: EventPostSchema = await event_service.validate_event(
                    dser_event,
                    priorities_mapping,
                    systems_mapping,
                )

                event_id: int | None = await event_service.insert(
                    event_for_insert,
                    user_id=None,
                    status_id=status_mapping["Новый"],
                    created_at=dser_event.created_at
                )

                if event_id and not await websocket_manager.is_empty_connections_list():
                    event_get: EventFullyJoinedSchema | None = await event_service.get_event_joined(event_id=event_id)
                    if event_get is None:
                        continue
                    await websocket_manager.broadcast_event(event_get)

    except EventValidationError as er:
        log.error(f"Event validation error: {er}")
    except KafkaError as e:
        log.error(f"Kafka error occurred: {e}")
    finally:
        log.info("Stopping Kafka consumer...")
        await consumer.stop()
        log.info("Kafka consumer stopped.")
