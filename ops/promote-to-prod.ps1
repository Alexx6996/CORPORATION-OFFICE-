Param(
  [string]$Version = "",
  [int]$HealthTimeoutSec = 60
)

$ErrorActionPreference = "Stop"

function Log($msg){ Write-Host ("[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg) }

$repoRoot = Split-Path -Parent $PSCommandPath
Set-Location $repoRoot

# 0) Контроль окружения и файлов
if (-not (Test-Path "$repoRoot\version.txt")){ throw "version.txt not found" }
if (-not (Test-Path "$repoRoot\.venv\Scripts\python.exe")){ throw ".venv not found at $repoRoot\.venv" }

# 1) Вычислить версию
if ([string]::IsNullOrWhiteSpace($Version)){
  $Version = (Get-Content "$repoRoot\version.txt" -Raw).Trim()
}
if ($Version -notmatch '^\d+\.\d+\.\d+$'){ throw "Invalid version: $Version (expected SemVer like 0.1.1)" }
Log "Target version: v$Version"

# 2) Сохранить текущий HEAD на всякий случай
$currRef = (git rev-parse --abbrev-ref HEAD) 2>$null
if (-not $currRef){ $currRef = (git rev-parse HEAD) }
Log "Current ref: $currRef"

# 3) Стоп службы
$svc = "AIOFFICESSvc"
Log "Stopping service $svc ..."
sc.exe stop $svc | Out-Null
Start-Sleep -Seconds 2

# 4) Обновить код до релизного тега
Log "Fetching tags ..."
git fetch --tags --prune
git checkout "v$Version"

# 5) Зависимости (pip)
$pip = "$repoRoot\.venv\Scripts\pip.exe"
Log "Installing dependencies (requirements.txt) ..."
if (Test-Path "$repoRoot\requirements.txt"){ & $pip install -r "$repoRoot\requirements.txt" }

# 6) Миграции (Alembic) — опционально
$py = "$repoRoot\.venv\Scripts\python.exe"
if (Test-Path "$repoRoot\db\alembic.ini" -or (Test-Path "$repoRoot\alembic.ini")){
  Log "Running alembic upgrade head ..."
  & $py -m alembic upgrade head
} else {
  Log "Alembic not configured — skipping"
}

# 7) Старт службы
Log "Starting service $svc ..."
sc.exe start $svc | Out-Null

# 8) Health-check
$healthUrl = "http://127.0.0.1:8181/healthz"
$deadline = (Get-Date).AddSeconds($HealthTimeoutSec)
$ok = $false
do {
  try {
    $resp = Invoke-WebRequest -Uri $healthUrl -UseBasicParsing -TimeoutSec 5
    if ($resp.StatusCode -eq 200){ $ok = $true; break }
  } catch { Start-Sleep -Milliseconds 500 }
} while ((Get-Date) -lt $deadline)

if (-not $ok){
  Log "Health probe failed. Rolling back to $currRef ..."
  sc.exe stop $svc | Out-Null
  git checkout $currRef
  sc.exe start $svc | Out-Null
  throw "Promote failed: health check didn't pass in ${HealthTimeoutSec}s"
}

Log "Promote OK: v$Version is healthy"
