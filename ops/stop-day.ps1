# ops/stop-day.ps1 — CORPORATION / OFFICE
# PowerShell 7+. Выполнять с правами Администратора.
$ErrorActionPreference = "Stop"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ssK"
$hostName = $env:COMPUTERNAME
$result = "OK"
$notes  = @()

Write-Host "=== STOP-DAY @ $ts on $hostName ==="

# 1) Остановить службу бекенда (если запущена)
try {
  $svc = Get-Service -Name "AIOFFICESSvc" -ErrorAction Stop
  if ($svc.Status -eq "Running") {
    Stop-Service -Name "AIOFFICESSvc" -Force -ErrorAction Stop
    Start-Sleep -Seconds 2
  }
  $svc = Get-Service -Name "AIOFFICESSvc"
  Write-Host "AIOFFICESSvc: $($svc.Status)"
  if ($svc.Status -ne "Stopped") { $result="ATTENTION"; $notes+="AIOFFICESSvc not stopped" }
} catch { $result="ATTENTION"; $notes+="Service AIOFFICESSvc not found or stop failed: $($_.Exception.Message)" }

# 2) Корректно остановить Redis-контейнер (если запущен)
try {
  $redis = (docker ps --format "{{.Names}}" | Select-String -Pattern "^aioffice-redis$").ToString()
  if ($redis) {
    docker stop aioffice-redis | Out-Null
    Start-Sleep -Seconds 2
  }
  $still = (docker ps --format "{{.Names}}" | Select-String -Pattern "^aioffice-redis$").ToString()
  Write-Host "Redis container running: " + ([string]::IsNullOrWhiteSpace($still) -eq $true ? "No" : "Yes")
  if ($still) { $result="ATTENTION"; $notes+="Redis container still running" }
} catch { $result="ATTENTION"; $notes+="Docker stop failed: $($_.Exception.Message)" }

# 3) Финальный статус / запись лога
$summary = if ($notes.Count -gt 0) { $notes -join "; " } else { "Stopped cleanly" }
$line = "[${ts}] RESULT: ${result} — ${summary}"
Write-Host $line

$logDir = Join-Path $PSScriptRoot "..\observability"
New-Item -ItemType Directory -Force $logDir | Out-Null
$logFile = Join-Path $logDir "stop-day.log"
$line | Out-File -FilePath $logFile -Append -Encoding utf8

exit ([int]($result -ne "OK"))
