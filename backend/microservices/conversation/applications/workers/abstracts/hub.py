from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type
from port import AbstractPort
from strategy import AbstractLBStrategy

TPort = TypeVar("TPort", bound=AbstractPort)


class AbstractHub(ABC, Generic[TPort]):

    @abstractmethod
    def get_available_port(self, alg="random") -> TPort:
        pass

    @abstractmethod
    def set_lb_strategy(self, ):
        pass

THub = TypeVar("THub", bound=AbstractHub)

class AbstractHubBuilder(ABC, Generic[THub]):

    @abstractmethod
    def set_maximum_port(self, capacity: int = 32):
        pass

    @abstractmethod
    def set_lb_strategy(self, strategy: Type[AbstractLBStrategy]):
        pass