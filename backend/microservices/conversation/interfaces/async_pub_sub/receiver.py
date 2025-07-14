from typing import Generic, Any
from abc import ABC, abstractmethod
from generic_types import TEvent
from multiprocessing import Queue

class IReceiver(ABC, Generic[TEvent]):
    @abstractmethod
    def receive(self) -> TEvent:
        pass

    @abstractmethod
    def chain_out(self, queue: Queue, signal: Any) -> bool:
        pass