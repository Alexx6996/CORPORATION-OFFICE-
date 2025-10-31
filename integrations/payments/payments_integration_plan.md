# Payments Integration Plan — CORPORATION / OFFICE

## Цели
- Приём платежей в sandbox → затем prod.
- Вебхуки провайдера → подтверждение платежей/возвратов.
- Фискализация: генерация контракта чека и отправка через ОФД.

## Потоки (draft)
1) Клиент инициирует оплату → фронт получает payment_intent.
2) Провайдер возвращает статус → бекенд /payments/webhook принимает событие.
3) При `payment.succeeded` → формируем receipt (see integrations/fiscal/receipt_model.yaml) → отправка в ОФД.
4) Логи и аудит: trace_id/span_id в JSON логах; запись исходных событий вебхука.

## Точки интеграции (бекенд)
- `POST /payments/charge` — sandbox-стаб, далее SDK провайдера.
- `POST /payments/webhook` — приём событий; проверка подписи (секрет из Credential Manager).
- Авторизация: OIDC/Basic через общую зависимость.

## Безопасность
- Секреты API и webhook — только в Windows Credential Manager (не в git).
- Ротация по расписанию: ops/secrets_rotation_schedule.yaml.
- Проверка подписи вебхуков: HMAC/подписи провайдера.

## Тестирование
- Юнит-тесты: tests/test_payments.py (health, charge, валидация).
- Интеграционные тесты на staging: провайдер sandbox, эмуляция вебхуков.

## Мониторинг
- Метрики: количество успешных/ошибочных чарджей, латентность.
- Алерты: доля 5xx > 1% за 15м (см. observability/alerts.yaml).

## План вывода в prod
- Staging PASS → релиз по prod_release_checklist.md.
- DR и rollback готовы (откат версии образа; отключение приёма платежей при инциденте).
