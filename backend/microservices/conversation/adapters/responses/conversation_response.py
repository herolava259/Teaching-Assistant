import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import date
from enum import IntEnum
from typing import Optional

class ResponseStatus(IntEnum):
    Success = 0
    Error = 1
    Neutral = 2

class ResponseMode(IntEnum):
    Debug = 0
    Production = 1
    Development = 2

class ConversationBaseResponse(BaseModel):
    entity_id: UUID = Field(..., description="id correspond with conversation entity")
    response_created_time: date
    status: ResponseStatus = Field(default=ResponseStatus.Success)
    description: Optional[str] = Field(...)
    mode: Optional[ResponseMode] = Field(...)

    @staticmethod
    def create_default(entity_id: UUID | None = None):
        if not entity_id:
            entity_id = uuid4()

        response = ConversationBaseResponse(entity_id = entity_id, response_created_time=datetime.datetime.now(),
                                            status = ResponseStatus.Neutral, mode = ResponseMode.Debug,
                                            description= None)

        return response

class ConversationQueryByIdResponse(ConversationBaseResponse):
    pass

