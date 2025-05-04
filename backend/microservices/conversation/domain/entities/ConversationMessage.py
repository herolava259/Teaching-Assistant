from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from domain.value_objects.Feedback import Feedback
from typing import Optional, List
from DocumentMetadata import DocumentMetadata



@dataclass(order=True)
class ConversationMessage:
    conversation_id: UUID
    chunk_id: UUID
    attendee_id: UUID
    reference_msg_id: UUID
    content: str
    created_at: date
    updated_at: date
    feedback: Optional[Feedback]
    deleted: bool = field(default = False)
    no_of_msg: int = field(default_factory=int, compare=True)
    documents: List[DocumentMetadata] = field(default_factory= list)
    id: UUID = field(default_factory=uuid4)

    @property
    def num_of_doc(self) -> int:
        return len(self.documents)
