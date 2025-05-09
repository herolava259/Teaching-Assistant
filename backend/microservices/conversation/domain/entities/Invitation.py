from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from BaseEntity import State
from enum import IntEnum
from typing import Optional
import datetime
from domain.entities.Attendee import Attendee


class EStatus(IntEnum):
    Pending = 0
    Accepted = 1
    Denied = 2
    Expired = 3


@dataclass
class Invitation:
    conversation_id: UUID
    inviter_id : UUID
    invitee_id : UUID
    due_date: date
    created_at: date
    state: State = field(default=State.NoAction)
    invitation_name: str = field(default='new lion')
    status: EStatus = field(default=EStatus.Pending)
    message: str = field(default='This is invitation from conversation host')
    id: UUID = field(default_factory=uuid4)

    def accept_invite(self) -> Optional[Attendee]:
        if self.status != EStatus.Pending:
            raise Exception(f"the invitation with id {self.id} cannot execute.")
        if self.due_date <= datetime.datetime.now():
            self.status = EStatus.Expired
            self.state = State.Updated
            return None

        self.status = EStatus.Accepted
        self.state = State.Updated
        return Attendee(self.invitee_id, self.conversation_id,
                        nickname=self.invitation_name,
                        state=State.Added,
                        created_date = datetime.datetime.now(),
                        updated_date= datetime.datetime.now())

    def refuse(self) -> bool:
        if self.status != EStatus.Pending:
            return False

        self.status = EStatus.Denied
        self.state = State.Updated
        return True