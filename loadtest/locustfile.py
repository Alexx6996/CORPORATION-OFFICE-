"""
AIOFFICE LOAD / STRESS PROFILE
Этот сценарий нагружает локальный observability probe aioffice
(uvicorn observability.metrics_app:app --host 127.0.0.1 --port 8001)

Назначение:
- Проверка, что /healthz остаётся доступным под параллельной нагрузкой.
- Проверка, что /metrics не деградирует по латентности при частом опросе.
- Фиксация базовой производительности как референс.

Важно:
- Это тестовый профиль нагрузки, запускается под User, .venv Active.
- Не трогает прод-службу, не требует Administrator.
"""

from locust import HttpUser, between, task


class AiofficeUser(HttpUser):
    host = "http://127.0.0.1:8001"
    wait_time = between(0.05, 0.2)  # агрессивно, почти спамим

    @task(5)
    def healthcheck(self):
        # базовый путь доступности
        self.client.get("/healthz", name="/healthz", timeout=2)

    @task(1)
    def scrape_metrics(self):
        # эмуляция Prometheus scrape
        self.client.get("/metrics", name="/metrics", timeout=5)
