from typing import Any, Dict, Callable, Tuple, override
import hashlib
import json
import pickle

class ValueTask:

    @staticmethod
    def get_hash_key(func: Callable, args: Tuple[Any,...], kwargs: Dict[str, Any]) -> str:
        func_data = {
            'name': func.__name__,
            'args': args,
            'kwargs': kwargs,
        }

        key_plain = json.dumps(func_data, sort_keys=True, default=str)
        return hashlib.sha256(key_plain.encode()).hexdigest()

    @staticmethod
    def unboxing_result(data: str) -> Any:
        state_data = json.loads(data)
        if not state_data['completed']:
            return None

        if state_data['type'] == 'json':
            return json.loads(state_data['result'])

        return pickle.loads(state_data['result'])

    def __init__(self, fn: Callable, args: Tuple[Any,...], kwargs: Dict[str, Any], on_completed: Callable = None):

        self.kwargs: Dict[str, object] = kwargs
        self.args: Tuple[Any,...] = args
        self.name: str = fn.__name__
        self.on_completed: Callable = on_completed
        self.result: Any = None
        self.completed: bool = False
        self.fn: Callable = fn

    @property
    def is_complete(self):
        return self.completed

    def __call__(self, on_completed:Callable = None) -> Any:
        if self.completed:
            return self.result
        self.result = self.fn(*self.args, **self.kwargs)
        self.completed = True

        if on_completed:
            self.on_completed = on_completed
        if self.on_completed:
            self.on_completed(self.result)
        return self.result

    def __str__(self):

        func_data = {
            'name': self.name,
            'args': self.args,
            'kwargs': self.kwargs,
        }

        key_plain = json.dumps(func_data, sort_keys=True, default=str)

        return key_plain

    def __hash__(self):
        key_plain = self.__str__()

        return hashlib.sha256(key_plain.encode()).hexdigest()

    def boxing_object(self) -> Tuple[str, Any]:
        key = self.__hash__()

        if not self.completed:
            return key, json.dumps({'completed': False,
                                    'on_completed': pickle.dumps(self.on_completed),
                                    "func": pickle.dumps(self.fn),
                                    "args": pickle.dumps(self.args),
                                    "kwargs": pickle.dumps(self.kwargs),
                                    'type': 'pickle'})

        data = {
            'completed': True,
            'result': pickle.dumps(self.result),
            'type': 'pickle'
        }

        return key, json.dumps(data)

    def boxing_data_only(self) -> Tuple[str, str]:

        key = self.__hash__()

        if not self.completed:
            return key, json.dumps({'completed': False,
                                    "args": json.dumps(self.args),
                                    "kwargs": json.dumps(self.kwargs),
                                    'type': 'json'})

        data = {
            'completed': True,
            'result': json.dumps(self.result),
            "args": json.dumps(self.args),
            "kwargs": json.dumps(self.kwargs),
            'type': 'json'
        }

        return key, json.dumps(data)


class ValueInstanceTask(ValueTask):
    def __init__(self, instance : Any, fn_name: str, args: Tuple[Any,...], kwargs: Dict[str, Any], on_completed: Callable = None):

        fn = getattr(instance, fn_name)
        super().__init__(fn, args, kwargs, on_completed)

        self.instance_type = type(instance)
        self.instance = type
        self.fn_name = fn_name


    @staticmethod
    def get_advanced_hash_key(instance: Any, instance_type: type, fn_name: str, args: Tuple[Any,...], kwargs: Dict[str, Any]) -> str:
        func_data = {
            'name': fn_name,
            'args': args,
            'kwargs': kwargs,
            "data_obj": instance.__dict__,
            "class_name": instance_type.__name__
        }

        key_plain = json.dumps(func_data, sort_keys=True, default=str)
        return hashlib.sha256(key_plain.encode()).hexdigest()

    def __str__(self):

        func_data = {
            'name': self.fn_name,
            'args': self.args,
            'kwargs': self.kwargs,
            "data_obj": self.instance.__dict__,
            "class_name": self.instance_type.__name__
        }

        key_plain = json.dumps(func_data, sort_keys=True, default=str)

        return key_plain

    @override
    def __call__(self, on_completed:Callable = None) -> Any:
        if self.completed:
            return self.result
        func = getattr(self.instance, self.fn_name)
        self.result = func(*self.args, **self.kwargs)
        self.completed = True

        if on_completed:
            self.on_completed = on_completed
        if self.on_completed:
            self.on_completed(self.result)
        return self.result

    @override
    def boxing_object(self) -> Tuple[str, Any]:
        key = self.__hash__()

        if not self.completed:
            return key, json.dumps({'completed': False,
                                    'on_completed': pickle.dumps(self.on_completed),
                                    "fn_name": self.fn_name,
                                    "args": pickle.dumps(self.args),
                                    "kwargs": pickle.dumps(self.kwargs),
                                    "instance_data": pickle.dumps(self.instance.__dict__),
                                    "instance_type": pickle.dumps(self.instance_type),
                                    'type': 'pickle'})

        data = {
            'completed': True,
            'result': pickle.dumps(self.result),
            'type': 'pickle'
        }

        return key, json.dumps(data)

    @override
    def boxing_data_only(self) -> Tuple[str, str]:

        key = self.__hash__()

        if not self.completed:
            return key, json.dumps({'completed': False,
                                    "args": json.dumps(self.args),
                                    "kwargs": json.dumps(self.kwargs),
                                    "instance_data": json.dumps(self.instance.__dict__),
                                    'type': 'json'})

        data = {
            'completed': True,
            'result': json.dumps(self.result),
            "instance_data": json.dumps(self.instance.__dict__),
            "args": json.dumps(self.args),
            "kwargs": json.dumps(self.kwargs),
            'type': 'json'
        }

        return key, json.dumps(data)
