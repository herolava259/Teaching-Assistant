from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date
from domain.aggregates.Pagination import OperationType, OrderType


class FilterConditionModel(BaseModel):
    operator: OperationType = Field(default=OperationType.LessThan)
    value: Union[str, date, int, float] = Field(default='created_date')

class FilterParamModel(BaseModel):
    field_name: str = Field(default='created_date')
    filter_conditions: List[FilterConditionModel] = Field(default_factory=list)

class OrderByClauseModel(BaseModel):
    order_type: OrderType = Field(default=OrderType.Ascending)
    order_by_fields: List[str] = Field(default_factory=list)

class PaginationParamsModel(BaseModel):

    page_size: int = Field(default=10, lt=100, gt=10)
    page_num: int = Field(default=0, ge=0)
    order_by_clause: Optional[OrderByClauseModel] = Field(default=None)
    distinct_by: List[str] = Field(default_factory=list)


class ConversationPaginationQuery(PaginationParamsModel):
    title_search_word: FilterConditionModel = Field(default=None)
    created_from_date_cond: date = Field(default_factory=list)
    created_to_date_cond: List[FilterConditionModel] = Field(default_factory=list)

