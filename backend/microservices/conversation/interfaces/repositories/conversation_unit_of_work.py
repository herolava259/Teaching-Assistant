from abc import ABC, abstractmethod
from domain.aggregates.Conversation import Conversation
from uuid import UUID
from typing import Optional

class IConversationUnitOfWork(ABC):

    @abstractmethod
    def get_conversation_aggregate(self, idx: UUID) -> Optional[Conversation]:
        pass
    @abstractmethod
    def update_conversation_domain(self, aggr_entity: Conversation) -> bool:
        pass
    @abstractmethod
    def remove_aggregate_by_id(self, idx: UUID) -> bool:
        pass

    @abstractmethod
    def remove_aggregate(self, entity: Conversation) -> bool:
        pass

    @abstractmethod
    def save_change(self) -> int:
        pass

