from dataclasses import dataclass, field
from uuid import UUID, uuid4
from BaseEntity import BaseEntity
from datetime import date
@dataclass
class Attendee:
    user_id: UUID
    conversation_id: UUID
    created_date: date
    id: UUID = field(default_factory=uuid4)



