from phoenix.otel import register
from utils import get_phoenix_endpoint
from openinference.instrumentation.openai import OpenAIInstrumentor


PROJECT_NAME = 'tracing-agent'



def setup_tracing(project_name = PROJECT_NAME, monitor_endpoint: str = ''):
    tracer_provider = register(project_name=PROJECT_NAME, endpoint= monitor_endpoint + 'v1/traces')
    OpenAIInstrumentor().instrument(tracer_provider = tracer_provider)

    ptracer = tracer_provider.get_tracer(__name__)

    return ptracer

tracer = setup_tracing(PROJECT_NAME, get_phoenix_endpoint())