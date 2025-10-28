# UTF-8 вывод
$enc = [System.Text.UTF8Encoding]::new($false); [Console]::OutputEncoding = $enc; $PSStyle.OutputEncoding = $enc

# Остановить backend (uvicorn app.main:app), запущенный под SYSTEM
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
  Where-Object { $_.CommandLine -match 'uvicorn app\.main:app' } |
  ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force } catch {} }

# Остановить Redis контейнер (если не нужен)
try { docker stop aioffice-redis | Out-Null } catch {}

Write-Host "Stop-day завершён." -ForegroundColor Yellow
