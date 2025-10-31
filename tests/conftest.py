"""
AIOFFICE TEST POLICY (applies to ALL tests in this repo)

1. Тесты принадлежат сервису "aioffice". Никаких упоминаний "Director" / "Директор".
2. В тестовых файлах допускается ТОЛЬКО Python-код.
   - Запрещено вызывать PowerShell / админские команды хоста из pytest.
   - Запрещено модифицировать систему, службы Windows, шифрование дисков, Docker и т.д.
3. Любые внешние HTTP-запросы должны быть замоканы.
   - Тесты не стучатся в реальный интернет и не используют реальные ключи.
   - Используем requests-mock или фикстуры.
4. Секреты, пароли, токены, ключи шифрования, реальные AIOFFICE_DB_URL не хардкодим в тесты.
   - Если нужны конфиги — делать фиктивные значения вида "DUMMY" или "test-token".
5. pytest запускается под контекстом User, внутри .venv проекта.
6. Интеграционные тесты, которые общаются с локальными компонентами (например, FastAPI app в памяти) допускаются.
   - Но нельзя дергать живую продуктивную службу, стоящую как Windows service.
"""

import pytest
import requests_mock


@pytest.fixture
def http_mock():
    """Глобальный мок для внешних HTTP-запросов.
    Пример:
        def test_svc(http_mock):
            with http_mock as m:
                m.get('https://external.service/api', json={'ok': True}, status_code=200)
                ...
    """
    with requests_mock.Mocker() as m:
        yield m
