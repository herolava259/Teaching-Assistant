from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from datetime import date

class PaginationParams(BaseModel):

    page_size: int = Field(default=10, lt=100, gt=10)
    page_num: int = Field(default=0, ge=0)


class ConversationPaginationQuery(PaginationParams):
    title_search_word: str = Field(default='')
    from_date: date = Field(...)
    to_date: date = Field(...)
