from pydantic import BaseModel, Field
from typing import List, Optional, Annotated


class PaginationParams(BaseModel):

    page_size: int = Field(default=10, lt=100, gt=10)
    page_num: int = Field(default=0, ge=0)