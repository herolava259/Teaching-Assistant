from typing import Dict, Self, Any
from ..containers.conversation import ConversationServiceContainer
from ..handlers.conversation import AbstractConversationHandler
from typing import get_type_hints, Type

class ConversationHandlerRegistry:
    def __init__(self, service_container: ConversationServiceContainer):
        self.operation_mapping: Dict = dict()
        self.service_provider: ConversationServiceContainer = service_container

    def register(self, handler_type: type, request_type: type| None = None) -> Self:
        if not request_type:
            self.operation_mapping[request_type] = handler_type
            return self

        return self

    def to_handler_mapper(self) -> Dict[type, Type[AbstractConversationHandler]]:
        def implement_handler(handler_type: type) -> Type[AbstractConversationHandler]:
            args_type = get_type_hints(handler_type.__init__)
            kwargs = {name_arg: self.service_provider.get_implementation_of_service(type_arg)
                    for name_arg, type_arg in args_type.items()}
            return handler_type(**kwargs)

        return {req_type: implement_handler(handler_type= handle_type) for req_type, handle_type in self.operation_mapping}



