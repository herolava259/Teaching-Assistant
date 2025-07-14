from generic_types import TEvent, TAsyncEventBus
from abc import ABC, abstractmethod
from typing import Generic

class ISubscriber(Generic[TEvent, TAsyncEventBus], ABC):

    @abstractmethod
    def subscribe(self, event_bus: TAsyncEventBus) -> bool:
        pass