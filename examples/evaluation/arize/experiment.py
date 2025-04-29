from example_agent.ExampleAgent import ExampleAgent
from examples.evaluation.arize.example_agent.setup_tracing import tracer
from utils import  get_openai_api_key
from opentelemetry.trace import StatusCode

def start_main_span(messages):
    experiment_agent = ExampleAgent(get_openai_api_key(), 'GPT4o-mini')
    print("Start main span with messages: ", messages)

    with tracer.start_as_current_span(
        'AgentRun', openinference_span_kind = 'agent'
    ) as span:
        span.set_input(value=messages)
        ret = experiment_agent.run_with_tracing(messages)
        print('Main span completed with return value: ', ret)
        span.set_output(value=ret)
        span.set_status(StatusCode.OK)
        return ret