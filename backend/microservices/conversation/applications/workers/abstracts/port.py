from typing import Generic
from abc import ABC, abstractmethod
from lb_metric import TProperty

class AbstractPort(ABC, Generic[TProperty]):

    @abstractmethod
    def metadata(self) -> TProperty:
        pass

    @abstractmethod
    def mark_connection(self):
        pass

    @abstractmethod
    def release_connection(self):
        pass

    @abstractmethod
    def acquire(self) -> bool:
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def put(self, data: str):
        pass

    @abstractmethod
    def push(self):
        pass

