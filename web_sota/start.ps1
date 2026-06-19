Param([switch]$Headless)

# --- SOTA Headless Standard ---
if ($Headless -and ($Host.UI.RawUI.WindowTitle -notmatch 'Hidden')) {
    Start-Process pwsh -ArgumentList '-NoProfile', '-File', $PSCommandPath, '-Headless' -WindowStyle Hidden
    exit
}
$WindowStyle = if ($Headless) { 'Hidden' } else { 'Normal' }
# ------------------------------

# bumi-mcp SOTA dashboard: FastAPI + MCP on 10774, Vite on 10775
$BackendPort = 10774
$FleetStartPath = Join-Path $RepoRoot "scripts\FleetStartMode.ps1"
if (-not (Test-Path -LiteralPath $FleetStartPath)) {
    Write-Host "ERROR: Missing vendored launcher helper: $FleetStartPath" -ForegroundColor Red
    exit 1
}
. $FleetStartPath

$FrontendPort = 10775
$ApiHealth = "http://127.0.0.1:$BackendPort/api/health"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$WebRoot = $PSScriptRoot

foreach ($port in @($BackendPort, $FrontendPort)) {
    $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($conn) {
        $conn | ForEach-Object {
            Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
        }
        Write-Host "Cleared port $port" -ForegroundColor Yellow
    }
}
Start-Sleep -Milliseconds 500

Write-Host "Starting bumi-mcp backend on :$BackendPort ..." -ForegroundColor Cyan
$null = Start-Process -FilePath "uv" `
    -ArgumentList "run", "python", "-m", "bumi_mcp", "--serve" `
    -WorkingDirectory $RepoRoot `
    -WindowStyle Minimized `
    -PassThru

$waited = 0
$ok = $false
while ($waited -lt 30) {
    try {
        $r = Invoke-WebRequest -Uri $ApiHealth -UseBasicParsing -TimeoutSec 2
        if ($r.StatusCode -eq 200) { $ok = $true; break }
    } catch { }
    Start-Sleep -Seconds 1
    $waited++
}
if (-not $ok) {
    Write-Host "WARN: Backend health not ready; continuing anyway." -ForegroundColor Yellow
}

Set-Location $WebRoot
if (-not (Test-Path "node_modules")) { npm install }

Write-Host "Starting Vite on :$FrontendPort ..." -ForegroundColor Cyan
$null = Start-Process -FilePath "cmd.exe" `
    -ArgumentList "/c", "npm run dev" `
    -WorkingDirectory $WebRoot `
    -WindowStyle Minimized `
    -PassThru

# 4b. Launch background task to open browser once frontend is ready (Auto-opened by Antigravity)
$frontendUrl = "http://127.0.0.1:$FrontendPort/"
$pollAndOpen = "for (`$i = 0; `$i -lt 60; `$i++) { try { `$null = Invoke-WebRequest -Uri '$frontendUrl' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; Start-Process '$frontendUrl'; exit } catch { Start-Sleep -Seconds 1 } }"
Start-Process powershell -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-Command", $pollAndOpen

Write-Host "Browser will open automatically when Vite is ready." -ForegroundColor Gray
Write-Host "Backend  $ApiHealth" -ForegroundColor Green
Write-Host "Frontend http://127.0.0.1:$FrontendPort" -ForegroundColor Green

