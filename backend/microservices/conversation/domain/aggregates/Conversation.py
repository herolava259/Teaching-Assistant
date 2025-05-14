import datetime
from functools import lru_cache
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from ..entities.Attendee import Attendee
from ..entities.MessageChunk import MessageChunk
from ..entities.BaseEntity import State
from ..entities.Invitation import Invitation


@dataclass
class Conversation:
    created_at: date
    updated_at: date
    created_user_id: UUID
    limit_invitation: int = field(default=10)
    deleted: bool = field(default=False)
    state: State = field(default=State.Added)
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

    @property
    def num_of_attendee(self) -> int:
        return len(self.attendees)
    @property
    def is_full(self) -> bool:
        return self.num_of_attendee > self.limit_invitation

    def user_in_conversation(self, user_id) -> bool:
        return any(a.user_id == user_id for a in self.attendees)

    def find_attendee(self, user_id) -> Optional[Attendee]:
        exist_obj: List[Attendee] = list(filter(lambda c: c.user_id == user_id, self.attendees))

        if not exist_obj:
            return None
        return exist_obj[0]

    def check_invitation(self, invitation: Invitation) -> bool:
        if self.is_full:
            return False

        if self.created_user_id != invitation.inviter_id:
            return False

        if any(c.user_id == invitation.invitee_id for c in self.attendees):
            return False

        return True




