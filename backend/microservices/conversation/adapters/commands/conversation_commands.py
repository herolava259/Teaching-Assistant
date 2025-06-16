from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional
from enum   import IntEnum

from ..base_requests import ConversationBaseRequest

class DeleteType(IntEnum):
    SoftDel = 1
    HardDel = 2
    PeriodicDel = 3


class ConversationCreateCommand(ConversationBaseRequest):
    title: str = Field(default='Conversation')
    limit_invitation: int = Field(default=10)
    created_user_id: UUID = Field(...)

class ConversationUpdateCommand(BaseModel):
    title: Optional[str]
    deleted_attendee_ids: Optional[List[str]]
    added_attendee_ids: Optional[List[str]]


class ConversationDeleteCommand(ConversationBaseRequest):
    type: DeleteType = DeleteType.HardDel
