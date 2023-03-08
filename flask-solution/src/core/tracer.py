from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace
from core.settings import get_settings

settings = get_settings()


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(resource=Resource.create(attributes={'service.name': 'auth'})))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.TRACER_HOST,
                agent_port=settings.TRACER_PORT,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
