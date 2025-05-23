from pydantic import BaseModel, Field
from typing import Optional

class ConversationBaseRequest(BaseModel):
    name: Optional[str] = Field(...)
