from typing import Any, Optional, List
from abc import ABC, abstractmethod
from uuid import UUID
from domain.aggregates.Conversation import Conversation

class IConversationRepository(ABC):

    @abstractmethod
    async def get_by_id(self, ids: UUID) -> Optional[Conversation]:
        pass

    @abstractmethod
    async def get(self, **filters: Any) -> Optional[Conversation]:
        pass

    @abstractmethod
    async def update(self, cons: Conversation) -> bool:
        pass

    @abstractmethod
    async def safety_update(self, cons: Conversation, params: List[str] | None) -> bool:
        pass

    @abstractmethod
    async def modify(self, cons: Conversation) -> bool:
        pass


