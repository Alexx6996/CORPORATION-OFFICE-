# BitLocker — статус шифрования (CORPORATION / OFFICE)

Аудит: 2025-10-31  
Хост: (заполнить при необходимости)

## Системный диск C:
- Статус: **FullyEncrypted**
- Алгоритм: **XtsAes256**
- Recovery Key: `C:\Secure\RecoveryKeys\C_recovery.txt`
- Доступ к `C:\Secure\RecoveryKeys\`: **только** локальные администраторы (SID `S-1-5-32-544`) и SYSTEM (`S-1-5-18`)
- Примечание: ключи **запрещено** хранить в git/облаках/почте.

## Рабочие диски (если есть, напр. F:)
- Статус: FullyEncrypted / Auto-unlock включён
- Recovery Key: `C:\Secure\RecoveryKeys\F_recovery.txt` (если применимо)

## Команды для проверки (источник отчёта)
```powershell
# Просмотр статуса
manage-bde -status C:
# Список рекавери-ключей (для аудита, НЕ прикладывать ключи в репозиторий)
(Get-BitLockerVolume -MountPoint 'C').KeyProtectors
Проверил(а): ДА

Дата: 31.10.2025
