from abc import ABC, abstractmethod
from generic_types import TEvent, TAsyncEventBus
from typing import Generic, Type

class IPublisher(ABC, Generic[TAsyncEventBus, TEvent]):

    @abstractmethod
    async def publish(self, event: TEvent) -> bool:
        pass
