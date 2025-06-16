from adapters.base_requests import ConversationBaseRequest
from adapters.responses.conversation_response import ConversationBaseResponse
from ..handlers.conversation import AbstractConversationHandler
from typing import Dict, Type


class ConversationMediator:
    def __init__(self, handler_mapper: Dict[type, Type[AbstractConversationHandler]]):
        self.handler_mapper: Dict[type, Type[AbstractConversationHandler]] = handler_mapper

    async def __execute__(self, request: Type[ConversationBaseRequest]) -> Type[ConversationBaseResponse]:

        req_type = type(request)

        if not self.handler_mapper.get(req_type, None):
            raise RuntimeError(f'Cannot implement or register handler of request type {req_type}')
        return await self.handler_mapper[req_type].handle(request)

    async def send(self, request: Type[ConversationBaseRequest]) -> Type[ConversationBaseResponse]:

        return await self.__execute__(request)