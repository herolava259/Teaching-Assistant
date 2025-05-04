import json
from typing import List


class Configuration(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file: str = "../configs/configurations.json"

        with open(self.config_file, mode = "r+") as file:
            self.update(json.load(file))


    def __setitem__(self, key, item):

        if self.__dict__.get(key, None) is not None:
            raise Exception(f"Cannot override existed with key = {key}")
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def bind(self, key: str | int, obj):

        if obj is None:
            raise Exception("obj argument should be not None here.")
        self.__dict__[key] = obj

    @staticmethod
    def load(path: str) -> int|str|dict:

        var_names: List[str] = path.split(':')

        config_object: dict | None = None

        with open('../configs/configurations.json') as file:
            config_object = json.load(file)

        result_obj = config_object

        for key in var_names:
            result_obj = result_obj[key]

        return result_obj
