import json
from pathlib import Path
import yaml

log_template_path = Path(__file__).parent.parent / "log_templates"
log_config_path = Path(__file__).parent.parent / "logging_configs"

class LoggingUtils:

    @staticmethod
    def load_json_file(path:str = "../log_templates/es_json_log_template.json") -> dict:

        with open(path, mode="r+") as file:
            json_object = json.load(file)

        return json_object

    @staticmethod
    def load_format_template_file(filename: str = "es_json_log_template.json") -> dict:

        specified_file_path = log_template_path / filename

        return json.loads(specified_file_path.read_text(encoding="utf-8"))

    @staticmethod
    def load_log_config_file(filename: str="5-queued-stderr-json-file.json") -> dict | None:

        specified_file_path = log_config_path / filename

        if not specified_file_path.exists() or not specified_file_path.is_file():
            raise FileNotFoundError(f"Cannot found file with name: {filename}")

        extension = specified_file_path.suffix

        if extension not in {".json", ".yaml"}:
            raise NotImplementedError(f"file type {extension} is not supported.")

        json_obj = None

        with specified_file_path.open("r+", encoding="utf-8") as file:
            json_obj = json.load(file) if extension == ".json" else yaml.safe_load(file)

        return json_obj


def load_template_config(file_name:str) -> dict:
    file_path = log_template_path / file_name

    with file_path.open("r+", encoding="utf-8") as file:
        template_obj = json.load(file)
    return template_obj


class LoggingTemplateConfig:
    def __init__(self):
        self.console_temp_obj = load_template_config("console_log_template.json")
        self.es_temp_obj = load_template_config("es_json_log_template.json")
        self.logstash_temp_obj = load_template_config("logstash_log_template.json")

    @property
    def console(self):
        return self.console_temp_obj

    @property
    def elastic_search(self):
        return self.es_temp_obj

    @property
    def logstash(self):
        return self.logstash_temp_obj
















