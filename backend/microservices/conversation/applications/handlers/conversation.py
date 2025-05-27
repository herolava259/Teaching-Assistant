from abc import ABC, abstractmethod
from adapters.base_requests import ConversationBaseRequest
from adapters.responses.conversation_response import ConversationBaseResponse
from typing import Dict, Self


class AbstractConversationHandler(ABC):

    @abstractmethod
    async def handle(self, request: ConversationBaseRequest) -> ConversationBaseResponse:
        pass
