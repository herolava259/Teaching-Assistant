from typing import Optional, Any, List
from uuid import UUID

from domain.aggregates.Conversation import Conversation
from interfaces.repositories.conversation_repository import IConversationRepository


class ConversationRepository(IConversationRepository):

    async def modify(self, cons: Conversation) -> bool:
        pass

    async def safety_update(self, cons: Conversation, params: List[str] | None) -> bool:
        pass

    async def update(self, cons: Conversation) -> bool:
        pass

    async def get(self, **filters: Any) -> Optional[Conversation]:
        pass

    async def get_by_id(self, ids: UUID) -> Optional[Conversation]:
        pass