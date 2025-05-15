from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from enum   import IntEnum

class DeleteType(IntEnum):
    SoftDel = 1
    HardDel = 2
    PeriodicDel = 3


class ConversationCreateCommand(BaseModel):
    title: str
    attendee_ids: List[UUID]

class ConversationUpdateCommand(BaseModel):
    title: Optional[str]
    deleted_attendee_ids: Optional[List[str]]
    added_attendee_ids: Optional[List[str]]


class ConversationDeleteCommand(BaseModel):
    type: DeleteType = DeleteType.HardDel
