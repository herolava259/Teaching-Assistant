from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class GeneralEvent:
    correlation_id: UUID = field(default_factory=uuid4)


@dataclass
class AbstractDomainEvent(GeneralEvent):
    source_domain_type: str = field(default="conversation")
    destination_domain_type: str = field(default="profile")


