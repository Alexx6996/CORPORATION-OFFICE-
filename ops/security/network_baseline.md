# ADR-002: Network Baseline (Reverse Proxy & Isolation)

**Дата:** 2025-10-31  
**Статус:** Accepted  
**Контекст:** Изоляция uvicorn (127.0.0.1:8181) от внешнего доступа. Внешний доступ только через reverse proxy.

## Решение
- **Reverse proxy:** Caddy (Windows service Caddy через NSSM).
- **Слушающие порты прокси (DEV):**
  - :8080 HTTP (временно, для устойчивого запуска и отладки).
  - :443 HTTPS — будет включён после загрузки валидных TLS-сертификатов.
- **Upstream:** 127.0.0.1:8181 (uvicorn/AIOFFICESSvc).
- **Службы:**
  - AIOFFICESSvc (uvicorn) — LocalService, автозапуск.
  - Caddy (reverse proxy) — LocalSystem (временно для DEV).
- **TLS-сертификаты:**
  - План: C:\Secure\TLS\fullchain.pem и C:\Secure\TLS\privkey.pem (права: SYSTEM/Админы).
  - На DEV сейчас **TLS OFF**. Включение — отдельный под-шаг после появления PEM.
- **Аутентификация фронтенда:**
  - На уровне приложения (OIDC/JWT), заголовки через прокси пробрасываются прозрачно.
- **Firewall:**
  - Разрешено: входящий TCP 8080 (DEV), TCP 443 (зарезервирован).
  - Заблокировано: входящий TCP 8181 (uvicorn), доступ только локально.

## Обоснование
- Разделяем внешний периметр и внутренний сервис: меньше площадь атаки.
- Прокси обеспечивает единое место для TLS/заголовков/политик.

## Последствия
- Операции идут через службу Caddy; uvicorn не публикуется наружу.
- Для prod требуется валидный TLS (PEM) или терминатор за корпоративным балансировщиком.

## Переход к HTTPS
После размещения PEM в C:\Secure\TLS\:
`caddyfile
:443 {
  tls C:\Secure\TLS\fullchain.pem C:\Secure\TLS\privkey.pem
  reverse_proxy 127.0.0.1:8181
}
Caddy
https://<host>/health
**2025-10-31**: HTTPS активен (PEM в C:\Secure\TLS), Caddy :443 → 127.0.0.1:8181.
