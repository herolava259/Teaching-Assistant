from abc import ABC, abstractmethod
from typing import Generic, Type, Self, List
from generic_types import TEvent
from subscriber import ISubscriber
from publisher import IPublisher
from uuid import UUID

class IAsyncEventBus(ABC, Generic[TEvent]):
    @abstractmethod
    async def publish(self, event: TEvent) -> bool:
        pass

    @abstractmethod
    async def signal(self, subscriber_id: UUID) -> bool:
        pass

    @abstractmethod
    async def consume(self, subscriber_id: UUID) -> List[TEvent]:
        pass

    @abstractmethod
    def subscribe(self, subscriber: Type[ISubscriber[TEvent, Self]]) -> UUID:
        pass

    @abstractmethod
    def register(self, publisher: Type[IPublisher[TEvent, Self]]) -> UUID:
        pass

    @abstractmethod
    def unsubscribe(self, subscriber_id: UUID) -> bool:
        pass

    @abstractmethod
    def unregister(self, publisher_id: UUID) -> bool:
        pass

