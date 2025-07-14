from abc import ABC, abstractmethod
from sender import ISender
from typing import Type, Union, Generic, Self, Iterable, Callable
from generic_types import TEvent, TTransformedResult, TPrimitiveResult, TInputPipeEvent, TOutputPipeEvent
from event import GeneralEvent


class IEventPipeInput(ABC, Generic[TEvent, TPrimitiveResult]):

    @abstractmethod
    def bind(self, sender: ISender) -> bool:
        pass

    @abstractmethod
    def passthrough(self, event: Union[TEvent, TPrimitiveResult]) -> Union[TEvent, TPrimitiveResult]:
        return event


class IEventPipeOutput(ABC, Generic[TTransformedResult, TPrimitiveResult]):

    @abstractmethod
    def bind(self, sender: ISender) -> bool:
        pass

    @abstractmethod
    def passthrough(self, event: Union[TTransformedResult, TPrimitiveResult]) -> Union[TTransformedResult, TPrimitiveResult]:
        pass

class IEventMiddlewareJoint(ABC, Generic[TEvent, TTransformedResult, TPrimitiveResult]):

    pipe_input: Union[Type[IEventPipeInput], Self]
    pipe_output: Type[IEventPipeOutput, Self]

    @abstractmethod
    def bind_pipe_input(self, pipe_input: Union[Type[IEventPipeInput], Self]):
        pass

    @abstractmethod
    def bind_pipe_output(self, pipe_output: Union[Type[IEventPipeOutput], Self]):
        pass

    @abstractmethod
    def transform(self, event: Union[TEvent, TTransformedResult]) -> Union[TEvent, TTransformedResult, TPrimitiveResult]:
        pass


class ISerializable(ABC, Generic[TEvent, TTransformedResult]):

    @abstractmethod
    def serialize(self, event: Union[TEvent, TTransformedResult]) -> TPrimitiveResult:
        pass



class IEventTransformationPipline(ABC, Generic[TInputPipeEvent, TOutputPipeEvent, TPrimitiveResult]):

    @abstractmethod
    def forward(self, event: TInputPipeEvent) -> Union[TOutputPipeEvent, TPrimitiveResult]:
        pass

class IEventPiplineBuilder(ABC, Generic[TInputPipeEvent, TOutputPipeEvent, TPrimitiveResult]):

    input_pipe : Type[IEventPipeInput[TInputPipeEvent, TPrimitiveResult]]
    output_pipe : Type[IEventPipeOutput[TOutputPipeEvent, TPrimitiveResult]]
    middleware_pipes : Iterable[Type[IEventMiddlewareJoint]]

    @abstractmethod
    def add_pipe(self, middleware_pipe: Type[IEventMiddlewareJoint]) -> Self:
        pass

    @abstractmethod
    def add_transform_func(self, fn: Callable[[Type[GeneralEvent]], Type[GeneralEvent]]) -> Self:
        pass

    @abstractmethod
    def add_sequence(self, pipes: Iterable[Type[IEventMiddlewareJoint]]) -> Self:
        pass

    @abstractmethod
    def build(self, *args, **kwargs) -> Type[IEventTransformationPipline]:
        pass






