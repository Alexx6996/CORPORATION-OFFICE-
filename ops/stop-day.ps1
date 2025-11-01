# ops/stop-day.ps1 — вечернее завершение смены
$ErrorActionPreference = "SilentlyContinue"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ssK"
Write-Host "=== STOP-DAY ($ts) ==="

# 1) Остановить службу AIOFFICESSvc
$svc = Get-Service -Name AIOFFICESSvc -ErrorAction SilentlyContinue
if ($svc) {
  if ($svc.Status -ne "Stopped") {
    Write-Host "[INFO] Stopping AIOFFICESSvc..."
    Stop-Service -Name AIOFFICESSvc -Force -ErrorAction SilentlyContinue
    Start-Sleep 2
  }
  Write-Host "[OK] AIOFFICESSvc: $((Get-Service -Name AIOFFICESSvc).Status)"
} else {
  Write-Host "[INFO] AIOFFICESSvc not found"
}

# 2) Погасить staging-контейнеры (если запущены)
$containers = @("aioffice-staging-app","aioffice-staging-redis")
foreach ($c in $containers) {
  $isRunning = docker ps --filter "name=$c" --filter "status=running" --format "{{.Names}}"
  if ($isRunning) {
    Write-Host "[INFO] Stopping container $c..."
    docker stop $c | Out-Null
  }
  $exists = docker ps -a --filter "name=$c" --format "{{.Names}}"
  if ($exists) {
    docker rm $c | Out-Null
    Write-Host "[OK] Container $c: removed"
  } else {
    Write-Host "[OK] Container $c: not present"
  }
}

# 3) Итог
Write-Host "RESULT: OK"
exit 0
