import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import date
from enum import IntEnum
from typing import Optional, List
from domain.aggregates.Conversation import Conversation

class ResponseStatus(IntEnum):
    Success = 0
    Error = 1
    Neutral = 2

class ResponseMode(IntEnum):
    Debug = 0
    Production = 1
    Development = 2

class ConversationBaseResponse(BaseModel):
    entity_id: Optional[UUID] = Field(description="id correspond with conversation entity", default=None)
    response_created_time: date = Field(default_factory=datetime.datetime.now)
    status: ResponseStatus = Field(default=ResponseStatus.Success)
    description: Optional[str] = Field(default='')
    mode: Optional[ResponseMode] = Field(default=ResponseMode.Debug)

    @staticmethod
    def create_default(entity_id: UUID | None = None):
        if not entity_id:
            entity_id = uuid4()

        response = ConversationBaseResponse(entity_id = entity_id, response_created_time=datetime.datetime.now(),
                                            status = ResponseStatus.Neutral, mode = ResponseMode.Debug,
                                            description= None)

        return response

class ConversationEntityResponse(ConversationBaseResponse):
    entity: Conversation

class ConversationSignalResponse(ConversationBaseResponse):
    signal: bool = Field(...)

    @staticmethod
    def return_failure(entity_id: UUID | None = None, description: str = 'Failure or False signal', status: ResponseStatus = ResponseStatus.Success,
                       mode: ResponseMode = ResponseMode.Debug):
        return ConversationSignalResponse(entity_id=entity_id,
                                          status=status,
                                          description=description,
                                          signal=False,
                                          mode = mode)

    @staticmethod
    def return_success(entity_id: UUID | None = None, description: str = 'Successful or True signal', status: ResponseStatus = ResponseStatus.Success,
                       mode: ResponseMode = ResponseMode.Debug):
        return ConversationSignalResponse(entity_id=entity_id,
                                          status=status,
                                          description=description,
                                          signal=True,
                                          mode = mode)


class ConversationPaginationResponse(ConversationBaseResponse):
    current_page: int = Field(...)
    total_page: int = Field(...)
    total_count: int = Field(...)
    data: List[Conversation] = Field(default_factory=list)


