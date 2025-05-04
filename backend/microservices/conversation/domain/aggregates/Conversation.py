import datetime
from functools import lru_cache
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from ..entities.Attendee import Attendee
from ..entities.MessageChunk import MessageChunk

@dataclass
class Conversation:
    created_at: date
    updated_at: date
    title: str = field(default="Conversation")
    chunks: List[MessageChunk] = field(default_factory=list)
    counter_chunk: int = field(default=0)
    attendees: List[Attendee] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)

    @property
    def num_of_msg(self) -> int:
        return sum(chunk.length for chunk in self.chunks)

    @property
    def num_of_chunk(self) -> int:
        return len(self.chunks)
    @property
    def latest_chunk(self) -> Optional[MessageChunk]:
        if not self.chunks:
            return None
        for chunk in self.chunks:
            if chunk.no_of_chunk == self.counter_chunk-1:
                return chunk
        return None

    def create_chunk(self) -> Optional[MessageChunk]:
        latest_chunk = self.latest_chunk

        if latest_chunk and not latest_chunk.is_full:
            return None

        new_chunk = MessageChunk(conversation_id=self.id,
                                 created_at=datetime.datetime.now(),
                                 no_of_chunk= self.counter_chunk,
                                 limit_length=20)

        return new_chunk
