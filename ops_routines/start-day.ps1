# CORPORATION / OFFICE
# start-day.ps1
# Утренний регламент проверки узла.
# ВЫПОЛНЯТЬ: PowerShell 7+ под АДМИН.

Write-Host "=== AIOFFICE START-DAY CHECK ==="

# Timestamp с часовым поясом
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
Write-Host "Timestamp: $timestamp"
Write-Host ""

# Информация о системе (версия Windows, кол-во логических CPU, объём ОЗУ)
try {
    $os = Get-CimInstance Win32_OperatingSystem
    $osVer = $os.Version
    $osCaption = $os.Caption
    $cpuCount = (Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum
    $memBytes = [int64]$os.TotalVisibleMemorySize * 1024
    Write-Host ("Server: {0} ({1}) | CPUs: {2} | Mem(bytes): {3}" -f $osVer, $osCaption, $cpuCount, $memBytes)
} catch {
    Write-Host "Server: N/A (failed to query system info): $($_.Exception.Message)"
}
Write-Host ""

# ---------------------------
# Проверка Redis (docker контейнер aioffice-redis)
# ---------------------------
$redisStatus = "DOWN"
try {
    $redisPing = docker exec aioffice-redis redis-cli ping 2>$null
    if ($redisPing -match "PONG") {
        $redisStatus = "OK"
        Write-Host "Redis: PONG"
    } else {
        $redisStatus = "WARN"
        Write-Host ("Redis: " + $redisPing)
    }
} catch {
    $redisStatus = "ERROR"
    Write-Host ("Redis: ERROR " + $_.Exception.Message)
}
Write-Host ""

# ---------------------------
# Проверка Windows-службы AIOFFICESSvc
# ---------------------------
$svcStatus = "DOWN"
$svc = Get-Service -Name "AIOFFICESSvc" -ErrorAction SilentlyContinue
if ($null -eq $svc) {
    $svcStatus = "MISSING"
    Write-Host "AIOFFICESSvc: NotFound"
} elseif ($svc.Status -eq "Running") {
    $svcStatus = "OK"
    Write-Host "AIOFFICESSvc: Running"
} else {
    $svcStatus = "WARN"
    Write-Host ("AIOFFICESSvc: " + $svc.Status)
}
Write-Host ""

# ---------------------------
# Проверка backend /health на локальном порту 8181
# НЕ КРИТИЧНО ДЛЯ RESULT
# ---------------------------
$healthHttpCode = "OFF"
$healthBody = "not running"
try {
    $healthResp = Invoke-WebRequest -UseBasicParsing -Uri "http://127.0.0.1:8181/health" -TimeoutSec 2
    $healthHttpCode = $healthResp.StatusCode
    $healthBody = $healthResp.Content.Trim()
} catch {
    # backend не поднят вручную — это нормальный сценарий,
    # не эскалируем в аварийный статус
}
Write-Host ("Backend /health: {0} {1}" -f $healthHttpCode, $healthBody)
Write-Host ""

# ---------------------------
# Итоговый RESULT
# ВНИМАНИЕ: backend /health НЕ влияет на аварийность
# ---------------------------
if ($redisStatus -eq "OK" -and $svcStatus -eq "OK") {
    Write-Host "RESULT: OK - core services are healthy."
} else {
    Write-Host "RESULT: ATTENTION - manual review required."
}

Write-Host ""
Write-Host "start-day done"
