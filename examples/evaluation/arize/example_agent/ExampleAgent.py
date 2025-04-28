from examples.evaluation.arize.example_agent.router import handle_tool_calls
from examples.evaluation.arize.example_agent.tools import tools
from openai import OpenAI
from examples.evaluation.arize.example_agent.prompts import SYSTEM_PROMPT
from typing import List

class ExampleAgent:
    def __init__(self, api_key: str, model_name: str):
        self.client: OpenAI = OpenAI(api_key = api_key)
        self.model_name: str = model_name
        self.messages:List[dict] = [{'role': 'system', 'content': SYSTEM_PROMPT}]

    def __call__(self, client_msg:str) -> str:

        self.messages.append({'role': 'user', 'content': client_msg})
        messages = self.messages
        while True:
            response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools)
            messages.append({'system': response.choices[0].message.content})

            tool_calls = response.choices[0].message.tool_calls

            if tool_calls:
                messages = handle_tool_calls(tool_calls, messages, self.client, self.model_name)
            else:
                return response.choices[0].message.content


