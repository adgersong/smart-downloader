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
# OTLP exporter (HTTP) for production – will use endpoint from Settings
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


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

    # Set up tracer provider – use OTLP exporter in production, console otherwise
    from ..core.config.settings import Settings
    settings = Settings()
    tracer_provider = TracerProvider(resource=resource)
    if settings.DEBUG:
        span_processor = BatchSpanProcessor(ConsoleSpanExporter())
    else:
        # Use OTLP HTTP exporter pointing to Jaeger endpoint
        span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_JAEGER_ENDPOINT))
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # Instrument FastAPI – this automatically creates spans for each request.
    FastAPIInstrumentor().instrument_app(app)

    # If you need Prometheus metrics, you can add a PrometheusMetricsExporter
    # and register it here. This minimal setup keeps dependencies light for now.

    # No return value – the side‑effects register the tracer globally.
    return None
