# ops/start-day.ps1 — CORPORATION / OFFICE
# PowerShell 7+. Выполнять с правами Администратора.
$ErrorActionPreference = "Stop"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ssK"
$hostName = $env:COMPUTERNAME
$result = "OK"
$notes  = @()

Write-Host "=== START-DAY CHECK @ $ts on $hostName ==="

# 1) Docker/Redis
try {
  $redis = (docker ps --format "{{.Names}} {{.Status}}" | Select-String -Pattern "^aioffice-redis\s").ToString()
  if ([string]::IsNullOrWhiteSpace($redis)) { $result="ATTENTION"; $notes+="Redis container 'aioffice-redis' not running" }
  Write-Host "Redis: $redis"
} catch { $result="ATTENTION"; $notes+="Docker not available: $($_.Exception.Message)" }

# 2) Служба бекенда
try {
  $svc = Get-Service -Name "AIOFFICESSvc" -ErrorAction Stop
  Write-Host "Service AIOFFICESSvc: $($svc.Status)"
  if ($svc.Status -ne "Running") { $result="ATTENTION"; $notes+="AIOFFICESSvc is not Running" }
} catch { $result="ATTENTION"; $notes+="Service AIOFFICESSvc not found" }

# 3) /healthz и /metrics
try {
  $h = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8181/healthz" -TimeoutSec 10
  if ($h.StatusCode -ne 200) { $result="ATTENTION"; $notes+="Healthz != 200 ($($h.StatusCode))" }
  $m = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8181/metrics" -TimeoutSec 10
  if ($m.StatusCode -ne 200) { $result="ATTENTION"; $notes+="Metrics != 200 ($($m.StatusCode))" }
  Write-Host "Healthz: $($h.StatusCode)  Metrics: $($m.StatusCode)"
} catch { $result="ATTENTION"; $notes+="Health/metrics check failed: $($_.Exception.Message)" }

# 4) Сроки секретов
try {
  $yamlPath = Join-Path $PSScriptRoot "..\ops\secrets_rotation_schedule.yaml"
  if (Test-Path $yamlPath) {
    $raw = Get-Content $yamlPath -Raw
    if ($raw -match "OVERDUE|DUE_TODAY") { $result="ATTENTION"; $notes+="Secrets rotation status requires action" }
  } else {
    $result="ATTENTION"; $notes+="secrets_rotation_schedule.yaml not found"
  }
} catch { $result="ATTENTION"; $notes+="Secret schedule read error: $($_.Exception.Message)" }

$summary = if ($notes.Count -gt 0) { $notes -join "; " } else { "All checks passed" }
$line = "[${ts}] RESULT: ${result} — ${summary}"
Write-Host $line

# Логируем итог
$logDir = Join-Path $PSScriptRoot "..\observability"
New-Item -ItemType Directory -Force $logDir | Out-Null
$logFile = Join-Path $logDir "start-day.log"
$line | Out-File -FilePath $logFile -Append -Encoding utf8

exit ([int]($result -ne "OK"))
