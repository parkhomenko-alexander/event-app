from datetime import date, timedelta

from celery import Celery
from celery.schedules import crontab

from settings import config

celery_app = Celery(
    __name__,
    broker=config.get_self_redis_uri(),
    backend=config.get_self_redis_uri(),
    include=[
        "tasks.building.tasks",
        # "tasks.data.tasks",
        # "tasks.tag.tasks",
    ],
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
)

# celery_app.conf.beat_schedule = {
#     "sync_history_data_every_2_hours": {
#         "task": "tasks.data.tasks.schedule_sync_history_data",
#         "schedule": crontab(minute="*/40"),
#         "kwargs": {"tag_title": "EnergyActiveForward30Min", "time_partition": "1month", "time_range": [(date.today() - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S"), (date.today() + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%S")]}
#     }
# }
