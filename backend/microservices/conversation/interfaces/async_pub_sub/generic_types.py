from typing import TypeVar


from event import GeneralEvent
from event_bus import IAsyncEventBus

TEvent = TypeVar("TEvent", bound=GeneralEvent)

TAsyncEventBus = TypeVar("TAsyncEventBus", bound=IAsyncEventBus)

TTransformedResult = TypeVar("TTransformedResult", bound=GeneralEvent)

TPrimitiveResult = TypeVar("TPrimitiveResult", float, int, str)

TInputPipeEvent = TypeVar("TInputPipeEvent", bound=GeneralEvent)
TOutputPipeEvent = TypeVar("TOutputPipeEvent", bound=GeneralEvent)



