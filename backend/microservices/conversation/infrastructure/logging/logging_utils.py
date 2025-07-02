import json


class LoggingUtils:

    @staticmethod
    def load_json_file(path:str = "../log_templates/json_log_template.json") -> dict:

        with open(path, mode="r+") as file:
            json_object = json.load(file)

        return json_object

