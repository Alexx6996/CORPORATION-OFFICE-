# Отключить basic_auth в Caddyfile и перезагрузить Caddy
$cf = Get-Content .\Caddyfile -Raw
$bak = "Caddyfile.rollback_{0}.bak" -f (Get-Date -Format 'yyyyMMdd_HHmmss')
Copy-Item .\Caddyfile $bak -Force
$cf2 = $cf -replace "(?ms)^\s*basic_auth\s*/\*\s*\{[^}]+\}\s*",""
$cf2 | Set-Content -Encoding UTF8 .\Caddyfile
C:\Tools\caddy.exe validate --config .\Caddyfile
if ($LASTEXITCODE -eq 0) { C:\Tools\caddy.exe reload --config .\Caddyfile; "BASIC_AUTH_DISABLED" } else { Copy-Item $bak .\Caddyfile -Force; "ROLLBACK_RESTORED" }
