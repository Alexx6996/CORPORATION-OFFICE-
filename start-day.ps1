# UTF-8 вывод в консоль
$enc = [System.Text.UTF8Encoding]::new($false); [Console]::OutputEncoding = $enc; $PSStyle.OutputEncoding = $enc

# Запустить Docker Desktop
Start-Process "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"

# Подождать ~60 сек и проверить Engine
Start-Sleep -Seconds 60
docker info --format "Server: {{.ServerVersion}} | CPUs: {{.NCPU}} | Mem: {{.MemTotal}}"

# Старт Redis
docker start aioffice-redis | Out-Null

# Проверка Redis
docker exec aioffice-redis redis-cli PING

# Если 8000 не слушается — попытаться запустить задачу (подавить ошибки доступа)
$ok = (Test-NetConnection -ComputerName localhost -Port 8000).TcpTestSucceeded
if (-not $ok) { try { schtasks /Run /TN "AIOFFICE\Backend" | Out-Null } catch {} ; Start-Sleep -Seconds 3 }

# Проверка порта и /health
$ok = (Test-NetConnection -ComputerName localhost -Port 8000).TcpTestSucceeded
if ($ok) { Invoke-RestMethod -Uri http://localhost:8000/health }

Write-Host "Start-day завершён." -ForegroundColor Green
