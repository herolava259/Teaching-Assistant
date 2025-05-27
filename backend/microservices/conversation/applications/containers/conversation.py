from typing import List, Dict, Any, Self, Callable, get_type_hints, Generic, TypeVar, Optional


class ServiceRegistration:
    def __init__(self, service_type: type, init_factory: Callable| None = None):
        self.service_type = service_type
        self.init_factory = init_factory
        self.arg_type_mapping = self.get_arguments_for_initialization()
        self.init_method: Callable | Any = None
        self.init_arg_table: Dict[str, Self] | None = None
        self.available: bool = False if not init_factory else True
        self.service_container: Optional['ConversationServiceContainer'] = None

    def get_arguments_for_initialization(self) -> dict:
        return get_type_hints(self.service_type.__init__)

    def get_dependencies(self) -> List[type]:
        types = set()
        for arg_type in self.arg_type_mapping.values():
            types.add(arg_type)
        return list(types)

    def add_construct_of_dependencies(self, impl_table: Dict[type, Self]):
        for arg_name, arg_type in self.arg_type_mapping.items():
            if not impl_table.get(arg_type, None):
                raise RuntimeError("Cannot register some service for necessary services for init the service")
            self.init_arg_table[arg_name] = impl_table[arg_type]

    def add_container(self, container: Optional['ConversationServiceContainer']):
        self.service_container = container

    def implement_service(self) -> Any:
        if self.init_factory:
            return self.init_factory(self.service_container)
        kwargs = {arg_name: self.init_arg_table[arg_name].implement_service() for arg_name in self.arg_type_mapping.keys()}
        return self.service_type(**kwargs)


class ConversationServiceContainer:

    def __init__(self, service_container: Dict[type, ServiceRegistration]):
        self.service_container: Dict[type, ServiceRegistration] = service_container

    def get_implementation_of_service(self, generic_service_type: type):
        if self.service_container.get(generic_service_type, None) is None:
            raise RuntimeError(f"The service {generic_service_type.__name__} is not register")
        return self.service_container[generic_service_type].implement_service()


class ConversationServiceRegistry:
    def __init__(self):
        self._container: Dict[type, ServiceRegistration] = dict()

    def register_service(self, instance_type: type, generic_type: type, factory_fn: Callable[[ConversationServiceContainer], Any]) -> Self:
        self._container[generic_type] = ServiceRegistration(service_type=instance_type, init_factory=factory_fn)

    def build_container(self) -> ConversationServiceContainer:
        from collections import deque, defaultdict
        from typing import Deque, DefaultDict
        dependency_table: DefaultDict[type, List[type]] = defaultdict(list)
        host_table: DefaultDict[type, List[type]] = defaultdict(list)
        for g_type in self._container.keys():
            dependency_table[g_type] = self._container[g_type].get_dependencies()
            for dependency in dependency_table[g_type]:
                host_table[dependency].append(g_type)

        in_deg: Dict[type, int] = {s_type: (len(dependencies) if not self._container[s_type].available else 0) for s_type, dependencies in dependency_table}
        zero_in_q: Deque[type] = deque()

        for s_type in in_deg.keys():
            if in_deg[s_type] == 0:
                zero_in_q.append(s_type)


        if not zero_in_q and dependency_table:
            raise RuntimeError("Circle dependency")
        while zero_in_q:
            cur_type = zero_in_q.popleft()
            self._container[cur_type].add_construct_of_dependencies(self._container)
            self._container[cur_type].available = True
            for dependency in host_table[cur_type]:
                in_deg[dependency] -= 1
                if in_deg[dependency] == 0:
                    zero_in_q.append(dependency)

        for key in in_deg:
            if in_deg[key] != 0:
                raise RuntimeError("Circle dependency")

        container = ConversationServiceContainer(dict(**self._container))

        for registration in self._container.values():
            registration.add_container(container)

        return container

from enum import IntEnum

class ImplementationType(IntEnum):
    Singleton = 1
    Scope = 2
    Transition = 3

TService = TypeVar('TService')
class ServiceFactory(Generic[TService]):
    pass
class SingletonServiceFactory(ServiceFactory):
    pass
class ScopedServiceFactory(ServiceFactory):
    pass
class TransitionServiceFactory(ServiceFactory):
    pass
