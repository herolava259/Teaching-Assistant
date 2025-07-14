from typing import Generic, Any
from abc import ABC, abstractmethod
from generic_types import TEvent
from multiprocessing import Queue

class ISender(ABC, Generic[TEvent]):
    @abstractmethod
    def send(self, event: TEvent) -> bool:
        pass

    @abstractmethod
    def chain_in(self, queue: Queue, signal: Any) -> bool:
        pass