$ts = Get-Date -Format "yyyyMMdd_HHmm"
$root = "C:\Secure\Backups\run_$ts"
New-Item -ItemType Directory -Force $root | Out-Null

$targets = @(
  @{Name="db";          Path="C:\Secure\Backups\db"},
  @{Name="vectorstore"; Path="C:\Secure\Backups\vectorstore"},
  @{Name="artifacts";   Path="C:\Secure\Backups\artifacts"}
)

foreach ($t in $targets) {
  $dst = Join-Path $root $t.Name
  New-Item -ItemType Directory -Force $dst | Out-Null
  if (Test-Path $t.Path) {
    robocopy $t.Path $dst /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
  }
}

$zip = "C:\Secure\Backups\AIOFFICE_full_$ts.zip"
Compress-Archive -Path "$root\*" -DestinationPath $zip -Force
Write-Output ("RESULT_ZIP: {0}" -f $zip)
