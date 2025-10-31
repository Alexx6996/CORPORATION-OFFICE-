# ops/secrets_check.ps1 — проверка статусов ротации секретов
# Возвращает 0 если всё OK, иначе 1 и пишет подробности в observability\secrets_check.log
$ErrorActionPreference = "Stop"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ssK"
$logDir = Join-Path $PSScriptRoot "..\observability"
New-Item -ItemType Directory -Force $logDir | Out-Null
$logFile = Join-Path $logDir "secrets_check.log"

$yamlPath = Join-Path $PSScriptRoot "..\ops\secrets_rotation_schedule.yaml"
if (-not (Test-Path $yamlPath)) {
  $line = "[$ts] ERROR: secrets_rotation_schedule.yaml not found"
  $line | Out-File -FilePath $logFile -Append -Encoding utf8
  Write-Host $line
  exit 1
}

$content = Get-Content $yamlPath -Raw
$issues = @()
if ($content -match "OVERDUE") { $issues += "OVERDUE present" }
if ($content -match "DUE_TODAY") { $issues += "DUE_TODAY present" }
if ($content -match "DUE_SOON") { $issues += "DUE_SOON present" }

if ($issues.Count -gt 0) {
  $line = "[$ts] ATTENTION: " + ($issues -join "; ")
  $line | Out-File -FilePath $logFile -Append -Encoding utf8
  Write-Host $line
  exit 1
} else {
  $line = "[$ts] OK: no due items"
  $line | Out-File -FilePath $logFile -Append -Encoding utf8
  Write-Host $line
  exit 0
}
