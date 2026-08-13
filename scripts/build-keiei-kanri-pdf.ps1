# Regenerates docs/keiei-kanri-guide-2026.pdf from keiei-kanri.html (Edge headless).
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$html = (Join-Path $root "keiei-kanri.html") -replace "\\", "/"
$url = "file:///" + $html
$dest = Join-Path $root "docs\keiei-kanri-guide-2026.pdf"
$tmp = Join-Path $env:USERPROFILE "keiei-kanri-guide-2026.pdf"
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) {
  $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
}
if (Test-Path $tmp) { Remove-Item $tmp -Force }
New-Item -ItemType Directory -Force -Path (Join-Path $root "docs") | Out-Null
Start-Process -FilePath $edge -ArgumentList @(
  "--headless", "--disable-gpu", "--no-pdf-header-footer",
  "--virtual-time-budget=20000", "--print-to-pdf=$tmp", $url
) -Wait
if (-not (Test-Path $tmp)) { throw "PDF was not created: $tmp" }
Copy-Item -Force $tmp $dest
Remove-Item -Force $tmp
Write-Output "Wrote $dest"
