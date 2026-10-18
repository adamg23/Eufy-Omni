# Vendors the client library (including generated protobuf modules) into the component.
# Run from the repo root:  powershell -NoProfile -ExecutionPolicy Bypass -File tools/deploy.ps1
# Upload is done by tools/upload_component.sh (File editor add-on ingress API).
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$comp = Join-Path $root 'custom_components\eufy_omni'
$vendor = Join-Path $comp 'eufy_omni_cloud'
if (Test-Path $vendor) { Remove-Item -Recurse -Force $vendor }
Copy-Item -Recurse (Join-Path $root 'eufy_omni_cloud') $vendor
Get-ChildItem -Recurse $vendor -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
Get-ChildItem -Recurse $vendor -File -Filter *.pyi | Remove-Item -Force
$count = (Get-ChildItem -Recurse $vendor -File | Measure-Object).Count
Write-Host "vendored client into $vendor ($count files)"
