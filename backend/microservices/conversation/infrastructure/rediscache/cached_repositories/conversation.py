from typing import Union, Optional, List, Dict, Any
from uuid import UUID

from domain.aggregates.Conversation import Conversation
from interfaces.repositories.conversation_repository import ICachedConversationRepository, IConversationRepository



class RedisCacheConversationRepository(ICachedConversationRepository):

    async def get_by_id(self, ids: UUID) -> Optional[Conversation]:
        pass

    async def get(self, **filters: Any) -> Optional[Conversation]:
        pass

    async def update(self, obj: Union[Conversation, Dict[str, Any]]) -> bool:
        pass

    async def safety_update(self, cons: Conversation, params: List[str] | None) -> bool:
        pass

    async def modify(self, cons: Conversation) -> bool:
        pass

    async def add(self, entity: Conversation) -> Optional[UUID]:
        pass

    async def total_conversation_of(self, user_id: UUID) -> int:
        pass

    async def remove(self, obj: Union[UUID, Conversation]) -> bool:
        pass