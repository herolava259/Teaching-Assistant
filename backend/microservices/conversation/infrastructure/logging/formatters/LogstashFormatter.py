from typing import Literal, Any
from infrastructure.logging.logging_utils import LoggingTemplateConfig
from logging import Formatter
from utils.enviroment_config import AppVariableConfig
from copy import deepcopy
from typing import override
from logging import LogRecord
import traceback
import datetime

logging_template_config = LoggingTemplateConfig()
variable_config = AppVariableConfig()
replaced_pairs = [(tag, tag.lower()) for tag in logging_template_config.logstash["complete"]["tags"]]


class LogstashFormatter(Formatter):
    def __init__(self, defaults: dict[str, Any], format_style: Literal["simple", "complete"] = "complete",
                 validate: bool = False):
        self.format_style = format_style
        self.config = deepcopy(logging_template_config.logstash[self.format_style])

        defaults = defaults if defaults else dict()

        defaults["service_name"] = variable_config.service
        defaults["service_no"] = variable_config.service_no

        super().__init__(fmt = self.config["format"],
                         datefmt=self.config["datefmt"], style=self.config["style"],
                         validate = validate,
                         defaults=defaults)

    def get_exc_fields(self, record: LogRecord):

        if record.exc_text:
            exc_info = record.exc_text
        elif record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = "None"
        return exc_info

    @classmethod
    def format_exception(cls, exc_info) -> str:
        return "".join(traceback.format_exception(*exc_info)) if exc_info else ''

    @override
    def format(self, record: LogRecord) -> str:
        def secure_replace(msg: str) -> str:
            for tag, replace in replaced_pairs:
                msg = msg.replace(tag, replace)
            return msg
        intersection = set(record.__dict__.keys()) & set(self.config["arguments"]) #optimize here

        data = {name: getattr(record, name) for name in intersection}
        data["service_name"] = variable_config.service
        data["service_no"] = variable_config.service_no
        data["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        data["message"] = secure_replace(record.getMessage())
        data["asctime"] = self.formatTime(record, self.datefmt)


        additional_data = {key_name: "None" for key_name in self.config["optional_fields"]["fields"]}

        if record.exc_info or record.exc_text:
            additional_data["exc_fields"] = secure_replace(self.get_exc_fields(record))

        if record.stack_info:
            additional_data["stack_fields"] = secure_replace(self.formatStack(record.stack_info))

        data["additional"] = self.config["optional_fields"]["format"] % additional_data
        result = self.config["format"] % data

        return result


if __name__ == "__main__":

    import logging

    logger = logging.getLogger(__name__)








