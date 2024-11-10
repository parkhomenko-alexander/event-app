import asyncio
from enum import Enum
from json import loads

from redis import RedisError
from redis.asyncio import Redis

from app.settings import config
from app.utils.logger import log


class CachePrefixes(Enum):
    BUILDINGS_ROOMS_INFO = "BUILDINGS_INFO"

class RedisManager:
    def __init__(self, redis_url: str | None = None):
        self.redis_client: Redis = Redis.from_url(redis_url or config.get_redis_buildings_cache_uri())

    def get_client(self):
        return self.redis_client

    async def close(self):
        await self.redis_client.close()

    async def ping(self) -> bool:
        try:
            response = await self.redis_client.ping()
            log.info(f"Redis cache ping response: {response}")
            return response
        except RedisError as e:
            log.error(f"Failed to ping Redis: {e}")
            return False

    async def get_cache_by_prefix(self, prefix: CachePrefixes):
        """
        Get all entries in the cache for a specific prefix.
        """
        try:
            cached_data = await self.redis_client.get(f"{prefix.value}")
            if cached_data:
                log.info(f"Cache hit for prefix: {prefix.value}")
                return cached_data
            log.info(f"Cache miss for prefix: {prefix.value}")
            return None
        except RedisError as e:
            log.error(f"Failed to get cache for prefix '{prefix.value}': {e}")
            return None