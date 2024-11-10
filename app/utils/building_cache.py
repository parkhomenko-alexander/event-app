import asyncio
import json
from time import sleep

import redis

from app.celery.tasks import buildings_cache
from app.utils.logger import log
from app.utils.redis_manager import CachePrefixes, RedisManager


class BuildingCache:
    _instance = None
    building_cache = {
        "title_id_building_cache": {},
        "id_title_building_cache": {}
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BuildingCache, cls).__new__(cls)
        return cls._instance

    def get_building_room_ids(self, building_title, room_title) -> tuple[int|None, int|None]:
        try:
            building_data = self.building_cache["title_id_building_cache"].get(building_title)
            if not building_data:
                return None, None
            building_id = building_data.get("id")
            rooms_data: dict = building_data["rooms"]
            if not rooms_data:
                return None, None
            room_id = rooms_data.get(room_title)
            return building_id, room_id
        except Exception as e:
            log.exception(f"An error occurred during cache update: {e}")
            return None, None
        
    def get_building_room_title(self, building_id, room_id) -> tuple[str|None, str|None]:
        try:
            building_data = self.building_cache["id_title_building_cache"].get(building_id)
            if not building_data:
                return None, None
            building_title = building_data.get("title")
            rooms_data: dict = building_data["rooms"]
            if not rooms_data:
                return None, None
            room_title = rooms_data.get(room_id)
            return building_title, room_title
        except Exception as e:
            log.exception(f"An error occurred during cache update: {e}")
            return None, None



    @classmethod
    def update_cache(cls, serialized_cache):
        try:
            title_id_building_cache = json.loads(serialized_cache)
            id_title_building_cache = {}
            for building in title_id_building_cache:
                rooms = title_id_building_cache[building]["rooms"]
                building_id = title_id_building_cache[building]["id"]
                    
                id_title_rooms = {}
                for room in rooms:
                    room_id = rooms[room]
                    id_title_rooms[room_id] = room

                id_title_building_cache[building_id] = {}
                id_title_building_cache[building_id]["title"] = building
                id_title_building_cache[building_id]["rooms"] = id_title_rooms

            if cls._instance:
                cls.building_cache["title_id_building_cache"] = title_id_building_cache
                cls.building_cache["id_title_building_cache"] = id_title_building_cache
        except Exception as e:
            log.exception(f"An error occurred: {e}")
            cls.building_cache = {
                "title_id_building_cache": {},
                "id_title_building_cache": {}
            } 

        
def get_building_cache():
    return BuildingCache()

async def update_chache(interval):
    redis_manager = RedisManager()
    manager = get_building_cache()

    while True:
        try:
            cache = await redis_manager.get_cache_by_prefix(prefix=CachePrefixes.BUILDINGS_ROOMS_INFO)
            if cache is None:
                log.error("Failed to fetch cache from Redis.")
            else:
                if manager:
                    manager.update_cache(cache)
                log.info("Building cache updated from Redis.")
        except Exception as e:
            log.exception(f"An error occurred during cache update: {e}")

        # Wait for the specified interval before the next update
        await asyncio.sleep(interval)

