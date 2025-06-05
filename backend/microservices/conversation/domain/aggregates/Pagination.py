from dataclasses import dataclass, field
from typing import TypeVar, Generic, List, Optional, Union, Set, Self
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

class ConditionBetweenType(int, Enum):
    And = 100_000_001
    Or = 100_000_002

class OrderType(int, Enum):
    Ascending = 100_000_001
    Descending = 100_000_002

@dataclass
class FilterCondition(Generic[TFilterValue]):
    operator: OperationType = field(default=OperationType.LessThan)
    value: TFilterValue = field(default=None)

@dataclass
class FilterParam(Generic[TFilterValue]):
    field_name: str = field(default='created_date')
    filter_conditions: List[FilterCondition[TFilterValue]] = field(default_factory=list)
    condition_between: ConditionBetweenType = field(default = ConditionBetweenType.And)

@dataclass
class OrderByClause:
    order_type: OrderType = field(default=OrderType.Ascending)
    order_by_fields: Set[str] = field(default_factory=set)

@dataclass
class PaginationDataCollection(Generic[TQueryEntity]):
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

    @property
    def actual_length_page(self) -> int:
        return len(self.data)

    def __len__(self):
        return self.actual_length_page

    @staticmethod
    def EmptyDataCollection(page_size: int = 10) -> Optional['PaginationDataCollection[TQueryEntity]']:
        return PaginationDataCollection(page_size=page_size)

@dataclass
class PaginationParams(Generic[TQueryEntity]):

    page_size: int = field(default=0)
    page_num: int = field(default=10)
    filter_params: List[FilterParam[Union[str, int, float, date]]] = field(default_factory=list)
    order_by_clauses: Optional[OrderByClause] = field(default=None)

    def example(self) -> TQueryEntity:
        pass

## Advanced pagination query
TQueryData = TypeVar('TQueryData')

class ConditionalFilterLeaf:
    def __init__(self,filter_param: FilterParam):
        self.filter_param = filter_param

class ConditionalFilterNode:
    def __init__(self, condition_between: ConditionBetweenType = ConditionBetweenType.And,
                 left_node: Union[None, 'ConditionalFilterNode', ConditionalFilterLeaf] = None,
                 right_node: Union[None, 'ConditionalFilterNode', ConditionalFilterLeaf] = None):
        self.condition_between: ConditionBetweenType = condition_between
        self.left_node = left_node
        self.right_node = right_node


@dataclass
class ConditionalFilterTree(Generic[TQueryEntity]):
    def __init__(self, root_node: ConditionalFilterNode):
        self.root = root_node


if __name__ == '__main__':
    empty_collection = PaginationDataCollection[int].EmptyDataCollection()
    print(empty_collection)
