from abc import ABC, abstractmethod
from lb_metric import TProperty, TScore, TMetric
from typing import Generic, Iterable, Type, Union
from uuid import UUID

class AbstractLBStrategy(ABC, Generic[TProperty,TMetric, TScore]):
    metric: TMetric
    @abstractmethod
    def promote_port(self, ports: Iterable[Union[Type[TProperty], TProperty]], **kwargs) -> UUID:
        pass