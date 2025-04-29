import os
from dotenv import load_dotenv, find_dotenv


def load_env():
    _ = load_dotenv(find_dotenv(), override=True)


def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key


def get_phoenix_endpoint():
    load_env()
    phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
    return phoenix_endpoint

def process_messages(messages):
    tool_calls = []
    tool_responses = []
    final_output = None

    for i, message in enumerate(messages):
        # Extract tool calls
        if 'tool_calls' in message and message['tool_calls']:
            for tool_call in message['tool_calls']:
                tool_name = tool_call['function']['name']
                tool_input = tool_call['function']['arguments']
                tool_calls.append(tool_name)

                # Prepare tool response structure with tool name and input
                tool_responses.append({
                    "tool_name": tool_name,
                    "tool_input": tool_input,
                    "tool_response": None
                })

        # Extract tool responses
        if message['role'] == 'tool' and 'tool_call_id' in message:
            for tool_response in tool_responses:
                if message['tool_call_id'] in message.values():
                    tool_response["tool_response"] = message['content']

        # Extract final output
        if message['role'] == 'assistant' and not message.get('tool_calls') and not message.get('function_call'):
            final_output = message['content']

    result = {
        "tool_calls": tool_calls,
        "tool_responses": tool_responses,
        "final_output": final_output,
        "unchanged_messages": messages,
        "path_length": len(messages)
    }

    return result