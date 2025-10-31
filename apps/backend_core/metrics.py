# apps/backend_core/metrics.py
from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest, PROCESS_COLLECTOR, PLATFORM_COLLECTOR
from prometheus_client import Counter

router = APIRouter()

# Базовые метрики процесса/платформы
_registry = CollectorRegistry()
PROCESS_COLLECTOR.reg_func(_registry)
PLATFORM_COLLECTOR.reg_func(_registry)

# Пример пользовательской метрики (счётчик запросов healthz)
health_requests_total = Counter("aioffice_health_requests_total", "Total healthz requests", registry=_registry)

@router.get("/metrics", summary="Prometheus metrics")
async def metrics() -> Response:
    output = generate_latest(_registry)
    return Response(output, media_type=CONTENT_TYPE_LATEST)

# Хук для healthz (импортируется в health.py при желании)
def inc_health_requests() -> None:
    health_requests_total.inc()
