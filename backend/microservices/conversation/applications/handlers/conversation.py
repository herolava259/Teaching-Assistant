from abc import ABC, abstractmethod
from adapters.base_requests import ConversationBaseRequest
from adapters.responses.conversation_response import ConversationBaseResponse



class AbstractConversationHandler(ABC):

    @abstractmethod
    async def handle(self, request: ConversationBaseRequest) -> ConversationBaseResponse:
        pass


class ConversationMediator:
    def __init__(self):
        pass

    def __execute__(self, request: ConversationBaseRequest) -> ConversationBaseResponse:
        pass
