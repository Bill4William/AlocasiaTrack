# build.ps1 — full release build for AlocasiaTrack
# Run from the project root:  .\build.ps1
#
# Steps:
#   1. Generate icon.ico
#   2. PyInstaller  → dist\AlocasiaTrack\
#   3. Inno Setup   → dist\installer\AlocasiaTrackSetup.exe

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Admin check ───────────────────────────────────────────────────────────────
# PyInstaller 6.x warns when run as Administrator; PyInstaller 7.x will block
# it entirely.  Catch this early with a clear message.
$currentPrincipal = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
if ($currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning @"

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  You are running this script as Administrator.                          │
  │  PyInstaller does not need (or want) admin privileges, and PyInstaller  │
  │  7.0 will BLOCK admin builds entirely.                                  │
  │                                                                         │
  │  Please close this terminal and reopen a normal (non-admin) PowerShell  │
  │  window, then run  .\build.ps1  again.                                  │
  └─────────────────────────────────────────────────────────────────────────┘
"@
    # Continue with a warning rather than aborting so existing workflows
    # aren't hard-broken — but the message makes it clear this must be fixed.
}

$ProjectDir = $PSScriptRoot
Set-Location $ProjectDir

# ── 1. Icon ───────────────────────────────────────────────────────────────
Write-Host "`n[1/3] Generating icon.ico ..." -ForegroundColor Cyan
$svgSource = "E:\AlocasiaTracker\AT_ICON.svg"
if (Test-Path $svgSource) {
    python scripts\svg_to_ico.py $svgSource icon.ico
} else {
    # Fallback to the procedurally-generated placeholder
    python scripts\make_icon.py
}
if ($LASTEXITCODE -ne 0) { throw "Icon generation failed." }

# ── 2. PyInstaller ────────────────────────────────────────────────────────
Write-Host "`n[2/3] Building with PyInstaller ..." -ForegroundColor Cyan
python -m PyInstaller AlocasiaTrack.spec --noconfirm --clean
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }

# ── 3. Inno Setup ─────────────────────────────────────────────────────────
Write-Host "`n[3/3] Compiling installer with Inno Setup ..." -ForegroundColor Cyan

$iscc = $null
foreach ($candidate in @(
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 5\ISCC.exe",
    "${env:ProgramFiles}\Inno Setup 5\ISCC.exe"
)) {
    if (Test-Path $candidate) { $iscc = $candidate; break }
}

if (-not $iscc) {
    Write-Warning "Inno Setup not found. Skipping installer step."
    Write-Host "Install from https://jrsoftware.org/isdl.php then re-run build.ps1."
} else {
    New-Item -ItemType Directory -Force -Path "dist\installer" | Out-Null
    & $iscc installer.iss
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup compilation failed." }
    Write-Host "`nInstaller ready: dist\installer\AlocasiaTrackSetup.exe" -ForegroundColor Green
}

Write-Host "`nBuild complete." -ForegroundColor Green
