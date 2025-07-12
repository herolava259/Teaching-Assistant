from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from IEvent import IEvent


TEvent = TypeVar("TEvent", bound=IEvent)

class IAsyncEventBus(ABC, Generic[TEvent]):

    def publish_async(self):