# OpenTelemetry instrumentation for FastAPI

"""Initialize OpenTelemetry tracing and metrics for the FastAPI application.

This module provides a simple `init_otel(app)` function that:
- Configures a `TracerProvider` with basic `Resource` attributes.
- Registers a `ConsoleSpanExporter` (replace with OTLP exporter in prod).
- Instruments the FastAPI app via `FastAPIInstrumentor`.
- Optionally, you can add Prometheus metric exporter or Jaeger exporter
  by extending the provider configuration.

The function is called from ``smart-downloader/backend/app/main.py`` after the
``FastAPI`` instance is created.
"""

from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
# For production you may use OTLP exporter:
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def init_otel(app: FastAPI) -> None:
    """Initialize OpenTelemetry tracing for the given FastAPI app.

    Parameters
    ----------
    app: FastAPI
        The FastAPI application instance.
    """
    # Resource attributes describe the service (useful for tracing backends)
    resource = Resource.create({
        "service.name": "smart-downloader",
        "service.version": "1.0.0",
    })

    # Set up a tracer provider with a simple console exporter.
    # Replace ``ConsoleSpanExporter`` with ``OTLPSpanExporter`` for
    # production environments (e.g., Jaeger, Tempo, or OpenTelemetry Collector).
    tracer_provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(ConsoleSpanExporter())
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # Instrument FastAPI – this automatically creates spans for each request.
    FastAPIInstrumentor().instrument_app(app)

    # If you need Prometheus metrics, you can add a PrometheusMetricsExporter
    # and register it here. This minimal setup keeps dependencies light for now.

    # No return value – the side‑effects register the tracer globally.
    return None
