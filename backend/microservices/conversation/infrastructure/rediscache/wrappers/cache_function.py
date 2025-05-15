import redis
from functools import wraps
from utils.configuration import Configuration
from typing import Callable
from adapters.tasks.ValueTask import ValueTask



class FunctionCacheService:
    def __init__(self, running_test = False):
        self.running_test = running_test
        self.redis_client = redis.Redis(host = Configuration.load('redis_cache:connections:default'), port=6379, db=0)

    def async_cache_fn(self, ttl: int = 30, enable: bool = True):
        def caching_decorator(func: Callable):
            @wraps(func)
            async def wrapper_function(*args, **kwargs):
                key = ValueTask.get_hash_key(func, args, kwargs)

                data: str = await self.redis_client.get(key)

                if data:
                    return ValueTask.unboxing_result(data)

                value_task = ValueTask(func, args, kwargs)

                value_task.__call__()

                key, data = value_task.boxing_object()

                await self.redis_client.setex(name=key, value=data, time=ttl)

                return value_task.result

            if not enable or self.running_test:
                return func
            return wrapper_function

        return caching_decorator




