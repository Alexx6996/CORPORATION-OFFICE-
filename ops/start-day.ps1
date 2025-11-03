# ops\start-day.ps1 — CORPORATION / OFFICE (canonical, port 8181)
# Context: Administrator, PowerShell 7+, .venv inactive
$ErrorActionPreference = "Stop"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "=== START-DAY CHECK ($ts) ==="

# 1) Docker & Redis
$redis = (docker ps -a --filter "name=aioffice-redis" --format "{{.Names}} {{.Status}}") 2>$null
if (-not $redis) { Write-Host "[ATTENTION] Redis container not found: aioffice-redis"; $redisOk = $false } else {
  Write-Host "[INFO] Redis: $redis"
  $redisOk = $redis -match "Up "
  if (-not $redisOk) {
    try { docker start aioffice-redis | Out-Null; Start-Sleep 2; $redisOk = ((docker ps --filter "name=aioffice-redis" --format "{{.Status}}") -match "Up ") } catch {}
  }
}
if ($redisOk) { Write-Host "[OK] Redis is Up" } else { Write-Host "[ATTENTION] Redis is not running" }

# 2) Windows service AIOFFICESSvc
$svc = Get-Service -Name "AIOFFICESSvc" -ErrorAction SilentlyContinue
if (-not $svc) { Write-Host "[ATTENTION] Service AIOFFICESSvc not found"; $svcOk=$false } else {
  Write-Host ("[INFO] Service: {0} ({1})" -f $svc.DisplayName, $svc.Status)
  if ($svc.Status -ne 'Running') {
    try { Start-Service -Name "AIOFFICESSvc"; Start-Sleep 2 } catch {}
    $svc = Get-Service -Name "AIOFFICESSvc" -ErrorAction SilentlyContinue
  }
  $svcOk = $svc.Status -eq 'Running'
  if ($svcOk) { Write-Host "[OK] Service Running" } else { Write-Host "[ATTENTION] Service NOT Running" }
}

# 3) Liveness /healthz on 127.0.0.1:8181
$healthzOk = $false
try {
  $r = Invoke-WebRequest -NoProxy -Uri "http://127.0.0.1:8181/healthz" -UseBasicParsing -TimeoutSec 3
  if ($r.StatusCode -eq 200) { $healthzOk = $true; Write-Host "[OK] /healthz 200" } else { Write-Host "[ATTENTION] /healthz status: $($r.StatusCode)" }
} catch { Write-Host "[ATTENTION] /healthz error: $($_.Exception.Message)" }

# 4) Result
if ($redisOk -and $svcOk -and $healthzOk) { Write-Host "RESULT: OK" } else { Write-Host "RESULT: ATTENTION" }

