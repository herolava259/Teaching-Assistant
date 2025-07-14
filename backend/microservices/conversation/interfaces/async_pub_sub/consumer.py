from typing import Generic
from abc import ABC, abstractmethod
from generic_types import TEvent

class IConsumer(Generic[TEvent], ABC):

    @abstractmethod
    async def consume(self, event):
        pass


