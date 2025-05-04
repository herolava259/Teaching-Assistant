from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import date
from ConversationMessage import ConversationMessage
from typing import List, Optional

@dataclass(order=True)
class MessageChunk:
    conversation_id: UUID
    created_at: date
    no_of_chunk: int = field(compare= True)
    limit_length: int = field(default=20)
    messages: List[ConversationMessage] = field(default_factory=list, compare=False)
    length: int = field(default=0, compare = False)
    id: UUID = field(default_factory=uuid4)

    @property
    def is_full(self) -> bool:
        return self.limit_length <= self.length

    @property
    def num_of_document(self) -> int:
        return sum(msg.num_of_doc for msg in self.messages)


    @property
    def latest_msg(self) -> Optional[ConversationMessage]:
        if self.length == 0:
            return None

        for msg in self.messages:
            if msg.no_of_msg == self.length-1:
                return msg
        return None
