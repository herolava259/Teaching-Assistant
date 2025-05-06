from dataclasses import dataclass, field
from uuid import UUID, uuid4
from BaseEntity import BaseEntity
from datetime import date
from BaseEntity import State
import random

@dataclass
class Attendee:
    user_id: UUID
    conversation_id: UUID
    created_date: date
    updated_date: date
    nickname: field(default_factory=lambda: f"rabbit-{random.randint(0,100)}")
    deleted: bool = field(default=False)
    state: State = field(default=State.Added)
    id: UUID = field(default_factory=uuid4)

