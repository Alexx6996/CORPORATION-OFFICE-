# Promote to Prod (AIOFFICESSvc)

## Preconditions
- BitLocker включён, ключи в C:\Secure\RecoveryKeys (см. ops\security\bitlocker_status.md)
- Служба AIOFFICESSvc установлена и работает
- .venv (Python 3.11) присутствует в репозитории
- version.txt содержит целевую SemVer-версию; в репозитории есть тег vX.Y.Z

## Команда
Администратор | cd C:\work\AICORPORATION\AIOFFICE | .venv: Не Активен
## Что делает скрипт
1. Останавливает AIOFFICESSvc
2. `git fetch --tags` и `git checkout vX.Y.Z`
3. `pip install -r requirements.txt` в локальную .venv
4. Alembic `upgrade head` (если конфиг есть)
5. Запускает AIOFFICESSvc и ждёт `/healthz` до 60 секунд
6. В случае неуспеха откатывается на предыдущий ref и поднимает службу

## Журналы
- Логи службы: `observability\aiofficessvc.log`
- Состояние здоровья: `http://127.0.0.1:8181/healthz`
