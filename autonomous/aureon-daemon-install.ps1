
# Aureon Local Daemon Installer
# This script installs and runs the Aureon local daemon for PowerShell integration

$ErrorActionPreference = "Stop"

# Colors for output
$Green = @{ForegroundColor='Green'}
$Yellow = @{ForegroundColor='Yellow'}
$Red = @{ForegroundColor='Red'}

Write-Host "⚡ Aureon Local Daemon Installer" @Yellow
Write-Host "=================================" @Yellow
Write-Host ""

# Check if daemon directory exists
$DaemonDir = "$env:APPDATA\Aureon\Daemon"
if (-not (Test-Path $DaemonDir)) {
    Write-Host "📁 Creating daemon directory..." @Green
    New-Item -ItemType Directory -Path $DaemonDir -Force | Out-Null
}

# Check if daemon is already running
$DaemonProcess = Get-Process -Name "aureon-daemon" -ErrorAction SilentlyContinue
if ($DaemonProcess) {
    Write-Host "✓ Aureon daemon is already running!" @Green
    exit 0
}

# Create a simple daemon script that listens for commands
$DaemonScript = @"
# Aureon Local Daemon v1.0
# Listens on localhost:8765 for commands from Aureon companion

\$port = 8765
\$listener = New-Object System.Net.HttpListener
\$listener.Prefixes.Add("http://localhost:\$port/")
\$listener.Start()

Write-Host "✓ Aureon daemon running on localhost:\$port" -ForegroundColor Green
Write-Host "Listening for commands from Aureon companion..." -ForegroundColor Cyan

while (\$true) {
    try {
        \$context = \$listener.GetContext()
        \$request = \$context.Request
        \$response = \$context.Response
        
        if (\$request.RawUrl -like "/execute*") {
            \$command = [System.Web.HttpUtility]::UrlDecode(\$request.QueryString["cmd"])
            
            # Execute the command
            \$output = ""
            try {
                \$output = Invoke-Expression \$command 2>&1 | Out-String
            } catch {
                \$output = "Error: \$(\$_.Exception.Message)"
            }
            
            \$response.ContentType = "application/json"
            \$body = @{ success = \$true; output = \$output } | ConvertTo-Json
            \$bytes = [System.Text.Encoding]::UTF8.GetBytes(\$body)
            \$response.OutputStream.Write(\$bytes, 0, \$bytes.Length)
        } elseif (\$request.RawUrl -eq "/status") {
            \$response.ContentType = "application/json"
            \$body = @{ status = "running"; timestamp = Get-Date } | ConvertTo-Json
            \$bytes = [System.Text.Encoding]::UTF8.GetBytes(\$body)
            \$response.OutputStream.Write(\$bytes, 0, \$bytes.Length)
        }
        
        \$response.Close()
    } catch {
        Write-Host "Error: \$(\$_.Exception.Message)" -ForegroundColor Red
    }
}
"@

# Save the daemon script
$DaemonScriptPath = "$DaemonDir\daemon.ps1"
Set-Content -Path $DaemonScriptPath -Value $DaemonScript -Force
Write-Host "✓ Daemon script created at: $DaemonScriptPath" @Green
Write-Host ""

# Start the daemon in the background
Write-Host "🚀 Starting Aureon daemon..." @Green
Start-Process powershell -ArgumentList "-WindowStyle Hidden -ExecutionPolicy Bypass -File \"$DaemonScriptPath\"" -NoNewWindow
Start-Sleep -Milliseconds 500

# Verify daemon is running
$DaemonProcess = Get-Process -Name powershell -ErrorAction SilentlyContinue | Where-Object { \$_.CommandLine -like "*daemon.ps1*" }
if (\$DaemonProcess) {
    Write-Host "✓ Aureon daemon is now running!" @Green
    Write-Host ""
    Write-Host "You can now give commands to Aureon from the companion chat." @Green
    Write-Host "Aureon will execute them on your local machine." @Green
} else {
    Write-Host "✗ Failed to start daemon. Please try again." @Red
    exit 1
}
