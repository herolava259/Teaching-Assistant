from router import handle_tool_calls
from external_tools import tools_schema
from openai import OpenAI
from prompts import SYSTEM_PROMPT
from examples.evaluation.arize.example_agent.setup_tracing import tracer
from typing import List
from opentelemetry.trace import StatusCode

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
            tools=tools_schema)
            messages.append({'system': response.choices[0].message.content})

            tool_calls = response.choices[0].message.tool_calls

            if tool_calls:
                messages = handle_tool_calls(tool_calls, messages, self.client, self.model_name)
            else:
                return response.choices[0].message.content


    def run_with_tracing(self, user_msg: str| List[dict]) -> List[dict]:
        if isinstance(user_msg, str):
            self.messages.append({'role': 'user', 'content': user_msg})
        elif isinstance(user_msg, list):
            self.messages.extend(user_msg)
        messages = self.messages
        while True:

            print("Starting router call span")
            
            with tracer.start_span(
                "router_call", openinference_span_kind="chain",
            ) as span:
                span.set_input(value=messages)

                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=tools_schema)
                messages.append({'system': response.choices[0].message.model_dump()})
                tool_calls = response.choices[0].message.tool_calls

                print("Receive response with tool calls: ", bool(tool_calls))
                span.set_status(StatusCode.OK)

                if tool_calls:
                    print("Starting tool calls span")
                    messages = handle_tool_calls(tool_calls, messages, self.client, self.model_name)
                    span.set_output(value=tool_calls)
                else:
                    print("No tool calls, returning final response")
                    span.set_output(value=response.choices[0].message.content)
                    return self.messages + [{'role': 'Assistant', 'content': response.choices[0].message.content}]



