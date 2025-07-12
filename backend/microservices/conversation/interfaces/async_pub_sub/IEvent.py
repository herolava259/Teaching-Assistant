from dataclasses import dataclass, field
from typing import Generic, Type
from uuid import UUID, uuid4

@dataclass
class IEvent:
    correlation_id: UUID = field(default_factory=uuid4)


