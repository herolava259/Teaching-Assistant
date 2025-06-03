from dataclasses import dataclass, field
from typing import TypeVar, Generic, List, Optional, Union, Set
from datetime import date

from enum import Enum

TQueryEntity = TypeVar('TEntity')
TFilterValue = TypeVar('TFilterValue', int, str, float, date)

class OperationType(int, Enum):
    LessThan = 100_000_001
    LessThanOrEqual = 100_000_002
    GreaterThan = 100_000_003
    GreaterThanOrEqual = 100_000_004
    Contain = 100_000_005
    Like = 100_000_006
    Equal = 100_000_007

class OrderType(int, Enum):
    Ascending = 100_000_001
    Descending = 100_000_002

class FilterCondition(dataclass, Generic[TFilterValue]):
    operator: OperationType = field(default=OperationType.LessThan)
    value: TFilterValue = field(default=None)

class FilterParam(dataclass, Generic[TFilterValue]):
    field_name: str = field(default='created_date')
    filter_conditions: List[FilterCondition[TFilterValue]] = field(default_factory=list)

class OrderByClause(dataclass):
    order_type: OrderType = field(default=OrderType.Ascending)
    order_by_fields: Set[str] = field(default_factory=set)

class PaginationDataCollection(dataclass, Generic[TQueryEntity]):
    page_num: int = field(default=0)
    page_size: int = field(default=10)

    data: List[TQueryEntity] = field(default_factory=list)

    total_record: int = field(default=0)

    @property
    def total_page(self) -> int:
        if self.page_size <= 0:
            raise RuntimeError('page is invalid (less than or equal to 0)')

        page_count = self.total_record // self.page_size

        return page_count + 1 if self.total_record % self.page_size != 0 else page_count

class PaginationParams(dataclass, Generic[TQueryEntity]):

    page_size: int = field(default=0)
    page_num: int = field(default=10)
    filter_params: List[FilterParam[Union[str, int, float, date]]] = field(default_factory=list)
    order_by_clauses: Optional[OrderByClause] = field(default=None)
    distinct_by: Set[str] = field(default_factory=set)

    def example(self) -> TQueryEntity:
        pass

