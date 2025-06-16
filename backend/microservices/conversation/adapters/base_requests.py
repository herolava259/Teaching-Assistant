from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class SecurityLevel(int, Enum):
    NonSense = 100_000_001
    Sense = 100_000_002
    Strict = 100_000_003

class ConversationBaseRequest(BaseModel):
    name: Optional[str] = Field(...)


class ConversationBaseCommandRequest(ConversationBaseRequest):
    created_time: Optional[date] = Field(...)
    security_level: SecurityLevel = Field(default=SecurityLevel.NonSense)
    hash_value: Optional[str] = Field(...)
    domain_type: Optional[str] = Field(default="Conversation")
    domain_id: Optional[str] = Field(...)
