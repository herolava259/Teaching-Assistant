from typing import Generic, TypeVar, Tuple
from abc import ABC, abstractmethod
from uuid import UUID
class BasePortProperty(ABC):
    id: UUID
    name: str
    weight: int

    @abstractmethod
    def get_report(self) -> dict:
        pass


TProperty = TypeVar("TProperty", bound=BasePortProperty)
TScore = TypeVar("TScore",int, float, None)

class AbstractPortMetric(ABC, Generic[TProperty, TScore]):

    @abstractmethod
    def compute_score(self, prop: TProperty) -> Tuple[UUID, TScore]:
        pass

TMetric = TypeVar("TMetric", bound=AbstractPortMetric)

