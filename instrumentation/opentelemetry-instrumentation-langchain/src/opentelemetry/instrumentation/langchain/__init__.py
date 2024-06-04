from typing import Collection
from wrapt import wrap_function_wrapper

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.langchain.package import _instruments
from opentelemetry.instrumentation.langchain.version import __version__
from opentelemetry.instrumentation.langchain.utils import _wrap_invoke, _wrap_response


class LangchainInstrumentor(BaseInstrumentor):
    """An instrumentor for kafka module
    See `BaseInstrumentor`
    """

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs):
        """Instruments the kafka module

        Args:
            **kwargs: Optional arguments
                ``tracer_provider``: a TracerProvider, defaults to global.
                ``request_hook``: a callable to be executed just before calling openai API
                ``response_hook``: a callable to be executed just after getting response from openai API
        """
        tracer_provider = kwargs.get("tracer_provider")
        request_hook = kwargs.get("request_hook")
        response_hook = kwargs.get("response_hook")

        tracer = trace.get_tracer(
            __name__,
            __version__,
            tracer_provider=tracer_provider,
            schema_url="https://opentelemetry.io/schemas/1.11.0",
        )

        wrap_function_wrapper(
            BaseChatModel, "invoke", _wrap_invoke(tracer, request_hook)
        )
        wrap_function_wrapper(
            ChatOpenAI, "_combine_llm_outputs", _wrap_response(tracer, response_hook)
        )
        wrap_function_wrapper(
            ChatOpenAI, "_create_chat_result", _wrap_response(tracer, response_hook)
        )

    def _uninstrument(self, **kwargs):
        pass