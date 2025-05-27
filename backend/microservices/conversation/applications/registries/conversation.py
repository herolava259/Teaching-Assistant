from typing import Dict, Self, Any

class ConversationOperationRegistry:
    def __init__(self):
        self.operation_mapping: Dict = dict()
        self.service_providers: list = []

    def register(self, request_type: type, handler: type) -> Self:
        self.operation_mapping[request_type] = handler
        return self

