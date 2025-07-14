from typing import override, Type, Self, List
from interfaces.async_pub_sub.event_bus import IAsyncEventBus
from multiprocessing import Queue
from interfaces.async_pub_sub.event import GeneralEvent
from uuid import UUID

from interfaces.async_pub_sub.publisher import IPublisher
from interfaces.async_pub_sub.subscriber import ISubscriber
from interfaces.async_pub_sub.generic_types import TEvent


class CrossThreadingEventBus(IAsyncEventBus[GeneralEvent]):

    def unsubscribe(self, subscriber_id: UUID) -> bool:
        pass

    def unregister(self, publisher_id: UUID) -> bool:
        pass

    def __init__(self):
        pass

    async def publish(self, event: TEvent) -> bool:
        pass

    async def signal(self, subscriber_id: UUID) -> bool:
        pass

    async def consume(self, subscriber_id: UUID) -> List[TEvent]:
        pass

    def subscribe(self, subscriber: Type[ISubscriber[TEvent, Self]]) -> UUID:
        pass

    def register(self, publisher: Type[IPublisher[TEvent, Self]]):
        pass

