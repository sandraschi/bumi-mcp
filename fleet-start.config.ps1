# Per-repo fleet start config for bumi-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'bumi-mcp'
    BackendPort  = 10774
    FrontendPort = 10775
    HealthPath   = '/api/health'
    WebRoot      = 'web_sota'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'bumi_mcp.app:app'
        SyncExtras    = @('dev')
        SyncOnStart  = $true
        Env           = @{ WEB_PORT = '10774' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
