from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from domain.value_objects.Feedback import Feedback
from typing import Optional, List
from LinkedDocumentMetadata import LinkedDocumentMetadata
from BaseEntity import State


@dataclass(order=True)
class ConversationMessage:
    conversation_id: UUID
    chunk_id: UUID
    attendee_id: UUID
    reference_msg_id: Optional[UUID]
    content: str
    created_at: date
    updated_at: date
    feedback: Optional[Feedback]
    state: State = field(default = State.Added)
    no_of_msg: int = field(default_factory=int, compare=True)
    documents: List[LinkedDocumentMetadata] = field(default_factory= list)
    id: UUID = field(default_factory=uuid4)

    @property
    def num_of_doc(self) -> int:
        return len(self.documents)
