import datetime

from pydantic import BaseModel, Field
from typing import List, Optional, Annotated, Literal
from uuid import UUID
from datetime import date
from paginations import PaginationParams

class ConversationGetByIdQuery(BaseModel):
    conversation_id: UUID = Field(...)


class ConversationQuery(BaseModel):

    title: Optional[str] = Field(default='There are conversation name')
    created_user_id: Optional[UUID] = Field(...)
    created_user_name: Optional[str] = Field(default='default bunny')
    created_since: Optional[date] = Field(default=datetime.datetime.now())


class TimeInterval(BaseModel):
    since_date: Optional[date] = Field(...)
    until_date: Optional[date] = Field(...)

class ConversationPaginationQuery(PaginationParams):

    title: Optional[str] = Field(default='')
    title_rule: Literal['contain', 'begin-with', 'end-with'] = Field(default='contain')

    occur_date: Optional[date] = Field(...)
    occur_rule: Literal['before', 'after', 'within-one-day'] = Field(default='before')

    within_interval: Optional[TimeInterval] = Field(...)
    interval_rule: Literal['include', 'exclude'] = Field(default='include')












