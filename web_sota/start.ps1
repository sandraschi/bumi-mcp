# bumi-mcp Vite dashboard (port 10775, proxies to 10774)
Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules")) {
    npm install
}
npm run dev
