from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


# Инициализируем провайдер трейсинга для aioffice.
# В проде сюда добавим OTLP-экспортёр в otel-collector.
def init_tracing():
    resource = Resource.create({
        'service.name': 'aioffice',
    })

    provider = TracerProvider(resource=resource)

    # Пока что — ConsoleSpanExporter, чтобы мы видели спаны прямо в выводе
    console_exporter = ConsoleSpanExporter()
    provider.add_span_processor(BatchSpanProcessor(console_exporter))

    # Делаем этого провайдера глобальным
    trace.set_tracer_provider(provider)

    # Вернём трейсер, чтобы можно было создавать спаны вручную
    return trace.get_tracer('aioffice')
