# CORPORATION / OFFICE
# stop-day.ps1
# Вечерний регламент остановки узла.
# ВЫПОЛНЯТЬ: PowerShell 7+ под АДМИН.

Write-Host "=== AIOFFICE STOP-DAY ==="
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
Write-Host "Timestamp: $timestamp"
Write-Host ""

# 1. Остановить службу AIOFFICESSvc
$svcStopped = $false
$svcObj = Get-Service -Name "AIOFFICESSvc" -ErrorAction SilentlyContinue
if ($null -eq $svcObj) {
    Write-Host "[SERVICE] AIOFFICESSvc not found (already gone?)"
    $svcStopped = $true
} else {
    if ($svcObj.Status -eq "Stopped") {
        Write-Host "[SERVICE] AIOFFICESSvc already Stopped"
        $svcStopped = $true
    } else {
        Write-Host "[SERVICE] Stopping AIOFFICESSvc..."
        try {
            Stop-Service -Name "AIOFFICESSvc" -Force -ErrorAction Stop
            Start-Sleep -Seconds 2
        } catch {
            Write-Host "[SERVICE] Stop-Service error: $($_.Exception.Message)"
        }
        $svcCheck = Get-Service -Name "AIOFFICESSvc" -ErrorAction SilentlyContinue
        if ($null -ne $svcCheck -and $svcCheck.Status -eq "Stopped") {
            $svcStopped = $true
            Write-Host "[SERVICE] AIOFFICESSvc Stopped"
        } else {
            Write-Host "[SERVICE] AIOFFICESSvc DID NOT STOP cleanly"
        }
    }
}
Write-Host ""

# 2. Остановить Redis контейнер
$redisStopped = $false
try {
    $isRunning = docker ps --filter "name=aioffice-redis" --format "{{.Names}}"
    if ([string]::IsNullOrWhiteSpace($isRunning)) {
        Write-Host "[REDIS] aioffice-redis already not running"
        $redisStopped = $true
    } else {
        Write-Host "[REDIS] Stopping aioffice-redis..."
        docker stop aioffice-redis 2>$null | Out-Null
        Start-Sleep -Seconds 2
        $stillRunning = docker ps --filter "name=aioffice-redis" --format "{{.Names}}"
        if ([string]::IsNullOrWhiteSpace($stillRunning)) {
            $redisStopped = $true
            Write-Host "[REDIS] aioffice-redis Stopped"
        } else {
            Write-Host "[REDIS] aioffice-redis DID NOT STOP cleanly"
        }
    }
} catch {
    Write-Host "[REDIS] docker stop error: $($_.Exception.Message)"
}
Write-Host ""

# 3. Финальный RESULT
if ($svcStopped -and $redisStopped) {
    Write-Host "RESULT: OK - node is safely shut down."
} else {
    Write-Host "RESULT: ATTENTION - check shutdown state manually."
}

Write-Host ""
Write-Host "stop-day done"
