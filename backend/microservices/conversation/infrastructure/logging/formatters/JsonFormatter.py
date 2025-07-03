import datetime
import json
import logging
from typing import override
import traceback
from dataclasses import dataclass, field
from typing import Optional, Union, Generic, TypeVar, Tuple, Dict, List
from enum import Enum
from ..logging_utils import LoggingUtils
from logging import LogRecord
from copy import deepcopy


TArgument = TypeVar("TArgument")
class FormatType(Enum, int):
    RegularExpr = 1
    DatetimeFmt = 2
    NumberType = 0


@dataclass
class ArgumentConfig(Generic[TArgument]):
    description: Optional[str] = field(default=None)
    format_type: FormatType = field(default=FormatType.RegularExpr)
    default: Optional[TArgument] = field(default=None)
    format: Optional[str] = field(default="")
    path: List[str] = field(default=None)
    type: Union[int, float, str] = field(default=0)
    limit: int = field(default=0)





class LoggingArgumentValidator:
    def __init__(self, arg_configs: Dict[str, ArgumentConfig], log_arguments: List[str]):

        self.arg_configs: Dict[str, ArgumentConfig] = arg_configs
        self.argument_names =  log_arguments

    def validate_all(self, *args, **kwargs) -> Tuple[bool, Dict[str, bool]]:

        from datetime import datetime
        import re
        def is_valid_datetime(s: str, fmt: str) -> bool:
            try:
                datetime.strptime(s, fmt)
                return True
            except ValueError:
                return False

        def _validate_item(config: ArgumentConfig, data: Union[int, float, str]) -> bool:
            if (config.type in ("str", "datetime") and not isinstance(data, str)) or \
                    (config.type == "number" and (not isinstance(data, int) or not isinstance(data, float))):
                return False

            if config.format_type == FormatType.RegularExpr \
                and config.format \
                and not re.fullmatch(config.format, data):
                return False
            if config.format_type == FormatType.DatetimeFmt \
                and config.format \
                and not is_valid_datetime(data, config.format):
                return False
            if config.type == "str" and len(data) > config.limit:
                return False

            return True
        validate_names = set(self.argument_names) & set(kwargs.keys())
        result = {arg_name: _validate_item(self.arg_configs[arg_name], kwargs[arg_name]) for arg_name in validate_names}
        return all(result.values()), result

# elk_args_validator = LoggingArgumentValidator(elk_argument_configs)

class JsonLogFactory:
    def __init__(self, template: dict, instructions: Dict[str, ArgumentConfig], log_arguments: List[str], need_validate: bool = False):
        self.template = template
        self.instructions = instructions
        self.validator: Optional[LoggingArgumentValidator] = LoggingArgumentValidator(instructions, log_arguments) if need_validate else None
        self.need_validate = need_validate
        self.log_arguments = set(log_arguments)
        self.template_str = json.dumps(template)

    def make_json_log(self, data: dict | LogRecord, **kwargs) -> str:


        args_in_record = set(self.log_arguments) & set(data.__dict__.keys())

        data: dict = {arg_name: data.__dict__[arg_name] for arg_name in args_in_record }

        ## override

        args_in_additional = set(self.log_arguments) & set(kwargs.keys())

        for arg_name in args_in_additional:
            data[arg_name] = kwargs[arg_name]

        if self.need_validate and not self.validator.validate_all(**data)[0]:
            raise RuntimeError(f"Log data are not valid.")

        clone_tmpl = deepcopy(self.template)

        # bind data
        for arg_name in self.log_arguments:
            instruction = self.instructions[arg_name]
            real_data = instruction.default if not data.get(arg_name, None) else data[arg_name]
            if instruction.type == "datetime" and isinstance(real_data, datetime.datetime):
                real_data = real_data.strftime(instruction.format)
            access_obj = clone_tmpl

            for p in instruction.path[:-1]:
                access_obj = access_obj[p]

            access_obj[instruction.path[-1]] = real_data

        return json.dumps(clone_tmpl)

    def fast_make_json_log(self, data: dict | LogRecord, **kwargs) -> str:
        args_in_record = set(self.log_arguments) & set(data.__dict__.keys())

        data: dict = {arg_name: data.__dict__[arg_name] for arg_name in args_in_record}

        ## override

        args_in_additional = set(self.log_arguments) & set(kwargs.keys())

        for arg_name in args_in_additional:
            data[arg_name] = kwargs[arg_name]

        for arg_name in self.log_arguments:
            instruction = self.instructions[arg_name]

            if not data.get(arg_name, None):
                data[arg_name] = instruction.default

            if instruction.type == "datetime" and isinstance(data[arg_name], datetime.datetime):
                data[arg_name] = data[arg_name].strftime(instruction.format)

        return self.template_str.format(**data)


def build_elk_log_factory() -> JsonLogFactory:
    elk_logging_object = LoggingUtils.load_format_template_file("es_json_log_template.json")

    elk_log_templ = elk_logging_object["json_log_template"]

    elk_arguments_data = elk_logging_object["instruction"]

    def load_argument_configs() -> Dict[str, ArgumentConfig]:
        kwargs = elk_arguments_data["details"]
        arg_table = dict()
        for name, item in kwargs.items():
            arg_obj = ArgumentConfig()
            for k, v in item.items():
                if k == "path":
                    v = v.split(":")
                setattr(arg_obj, k, v)
            arg_table[name] = arg_obj
        return arg_table

    elk_argument_configs = load_argument_configs()
    json_log_factory = JsonLogFactory(elk_log_templ, elk_argument_configs, elk_arguments_data["instruction"]["arguments"])
    return json_log_factory

elk_log_factory = build_elk_log_factory()


class ELKJsonFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_exc_fields(self, record: LogRecord):

        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text

        return exc_info

    @classmethod
    def format_exception(cls, exc_info) -> str:
        return "".join(traceback.format_exception(*exc_info)) if exc_info else ''

    @override
    def format(self, record: LogRecord, *args, **kwargs) -> str:
        if not kwargs:
            kwargs = dict()
        kwargs["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        kwargs["exc_fields"] = self.get_exc_fields(record)
        kwargs["message"] = record.getMessage()
        kwargs["created_time"] = datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc)
        kwargs["processName"] = record.name

        return elk_log_factory.make_json_log(record, **kwargs)



LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class NormalJSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": datetime.datetime.fromtimestamp(
                record.created, tz=datetime.timezone.utc
            ).isoformat(),
        }
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

        return message