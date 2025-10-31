# ops/release_prepare.ps1
param(
  [string]$Version = "0.1.0"
)
$ErrorActionPreference = "Stop"
git add -A
git commit -m "feat(release): prepare v$Version baseline" --allow-empty
git tag -a "v$Version" -m "Release $Version"
Write-Host "Created commit and tag v$Version. Push manually:"
Write-Host "git push && git push origin v$Version"
