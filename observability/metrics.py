from time import perf_counter

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
)

# отдельный реестр метрик для aioffice
registry = CollectorRegistry()

REQUEST_COUNT = Counter(
    'aioffice_request_total',
    'Total HTTP requests',
    ['endpoint', 'method', 'http_status'],
    registry=registry,
)

REQUEST_LATENCY = Histogram(
    'aioffice_request_latency_seconds',
    'Request latency (seconds)',
    ['endpoint', 'method'],
    registry=registry,
)

ERROR_COUNT = Counter(
    'aioffice_error_total',
    'Total 5xx responses',
    ['endpoint', 'method'],
    registry=registry,
)

def track_request(endpoint: str, method: str):
    start = perf_counter()
    def _finish(status_code: int):
        duration = perf_counter() - start
        REQUEST_COUNT.labels(endpoint=endpoint, method=method, http_status=str(status_code)).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint, method=method).observe(duration)
        if int(status_code) >= 500:
            ERROR_COUNT.labels(endpoint=endpoint, method=method).inc()
    return _finish

def render_metrics():
    output = generate_latest(registry)
    return CONTENT_TYPE_LATEST, output
