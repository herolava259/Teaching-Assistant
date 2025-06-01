from applications.containers.conversation import ConversationServiceContainer, ConversationServiceRegistry
from applications.handlers.conversation import *
from applications.mediators.conversation import ConversationMediator
from applications.registries.conversation import ConversationOperationRegistry
from interfaces.repositories.conversation_repository import IConversationRepository
from infrastructure.postgresqldb.repositories.ConversationRepository import ConversationRepository

def register_service() -> ConversationServiceRegistry:
    registry = ConversationServiceRegistry()

    return registry.register_service(ConversationRepository, IConversationRepository)


def register_handler(service_container: ConversationServiceContainer) -> ConversationOperationRegistry:
    handler_registry = ConversationOperationRegistry(service_container)
    handler_registry.register(ConversationGetByIdQueryHandler)
    return handler_registry

def create_mediator()->ConversationMediator:
    service_registry = register_service()
    service_container = service_registry.build_container()

    handler_registry = register_handler(service_container)
    handler_mapper = handler_registry.to_handler_mapper()
    mediator = ConversationMediator(handler_mapper)
    return mediator
