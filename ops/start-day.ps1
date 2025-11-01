# ops/start-day.ps1 — утренний чек системы
$ErrorActionPreference = "SilentlyContinue"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ssK"
Write-Host "=== START-DAY ($ts) ==="

# 1) Docker Desktop
$dockerv = docker version --format '{{.Server.Version}}'
if ($LASTEXITCODE -ne 0 -or -not $dockerv) { Write-Host "[ATTENTION] Docker not available"; $docker_ok=$false } else { Write-Host "[OK] Docker $dockerv"; $docker_ok=$true }

# 2) Redis контейнер
$redis = docker ps --filter "name=aioffice-staging-redis" --filter "status=running" --format '{{.Names}}'
if (-not $redis) { Write-Host "[ATTENTION] Redis container not running"; $redis_ok=$false } else { Write-Host "[OK] Redis: $redis"; $redis_ok=$true }

# 3) Служба AIOFFICESSvc
$svc = Get-Service -Name AIOFFICESSvc -ErrorAction SilentlyContinue
if (-not $svc) { Write-Host "[ATTENTION] Service AIOFFICESSvc not found"; $svc_ok=$false }
elseif ($svc.Status -ne 'Running') { Write-Host "[ATTENTION] Service AIOFFICESSvc: $($svc.Status)"; $svc_ok=$false }
else { Write-Host "[OK] Service AIOFFICESSvc: Running"; $svc_ok=$true }

# 4) Healthz локального бекенда
try {
  $code = (Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8181/healthz" -TimeoutSec 5).StatusCode
  if ($code -eq 200) { Write-Host "[OK] /healthz = 200"; $health_ok=$true } else { Write-Host "[ATTENTION] /healthz = $code"; $health_ok=$false }
} catch { Write-Host "[ATTENTION] /healthz unreachable: $($_.Exception.Message)"; $health_ok=$false }

# Итог
if ($docker_ok -and $redis_ok -and $svc_ok -and $health_ok) { Write-Host "RESULT: OK" ; exit 0 } else { Write-Host "RESULT: ATTENTION" ; exit 1 }
