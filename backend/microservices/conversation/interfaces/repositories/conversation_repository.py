from typing import Any, Optional, List, Union, Dict
from abc import ABC, abstractmethod
from uuid import UUID
from domain.aggregates.Conversation import Conversation

from domain.aggregates.Pagination import PaginationParams, PaginationDataCollection

class IConversationRepository(ABC):

    @abstractmethod
    async def get_by_id(self, ids: UUID) -> Optional[Conversation]:
        pass

    @abstractmethod
    async def get(self, **filters: Any) -> Optional[Conversation]:
        pass

    @abstractmethod
    async def update(self, obj: Union[Conversation, Dict[str, Any]]) -> bool:
        pass

    @abstractmethod
    async def safety_update(self, cons: Conversation, params: List[str] | None) -> bool:
        pass

    @abstractmethod
    async def modify(self, cons: Conversation) -> bool:
        pass

    @abstractmethod
    async def total_conversation_of(self, user_id: UUID) -> int:
        pass

    @abstractmethod
    async def add(self, entity: Conversation) -> Optional[UUID]:
        pass

    @abstractmethod
    async def remove(self, obj: Union[UUID, Conversation]) -> bool:
        pass

    @abstractmethod
    async def pagination_query(self, pagination_params: PaginationParams[Conversation]) -> PaginationDataCollection[Conversation]:
        pass



class ICachedConversationRepository(IConversationRepository, ABC):
    pass

