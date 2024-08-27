from functools import wraps


def with_repository_manager(f):
    @wraps(f)
    async def wrapper(self, *args, **kwargs):
        async with self.repository_manager:
            return await f(self, *args, **kwargs)
    return wrapper