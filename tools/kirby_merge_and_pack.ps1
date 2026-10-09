# Gop font Kirby bang FontForge roi dong goi lai mod.
#
# CACH DUNG:
#   1. Cai FontForge:  winget install FontForge      (hoac tai fontforge.org)
#   2. Chay file nay:  .\tools\kirby_merge_and_pack.ps1
#
# Script se: gop glyph tieng Viet tu Nunito vao 45 font -> dong goi lai vao mod.

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$ff = Get-Command fontforge -ErrorAction SilentlyContinue
if (-not $ff) {
    $tryPaths = @(
        "$env:ProgramFiles\FontForgeBuilds\bin\fontforge.exe",
        "${env:ProgramFiles(x86)}\FontForgeBuilds\bin\fontforge.exe",
        "$env:LOCALAPPDATA\Programs\FontForgeBuilds\bin\fontforge.exe"
    )
    foreach ($p in $tryPaths) { if (Test-Path $p) { $ff = $p; break } }
}
if (-not $ff) {
    Write-Host "KHONG TIM THAY fontforge." -ForegroundColor Red
    Write-Host "Cai bang:  winget install FontForge"
    Write-Host "hoac tai:  https://fontforge.org/en-US/downloads/"
    exit 1
}

Write-Host "FontForge: $ff"
Write-Host ""
Write-Host "Buoc 1/2: gop glyph tieng Viet vao font..."
& $ff -script "tools\kirby_merge_fonts.pe"

Write-Host ""
Write-Host "Buoc 2/2: dong goi lai vao mod (co doc lai xac minh)..."
python tools/kirby_font_reencrypt.py

Write-Host ""
Write-Host "XONG. Chep output\atmosphere\contents\01004D300C5AE000\ vao the nho de test." -ForegroundColor Green
