from typing import Generic
from generic_types import TEvent
from abc import ABC, abstractmethod

class IWorkerHandler(ABC, Generic[TEvent]):

    @abstractmethod
    async def handle(self, event: TEvent):
        pass
