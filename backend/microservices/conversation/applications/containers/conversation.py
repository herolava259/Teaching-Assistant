from typing import List, Dict, Any, Self

class ConversationServiceContainer:
    def __init__(self):
        self._container: Dict[type, Any] = dict()

    def add_service(self) -> Self:
        pass
