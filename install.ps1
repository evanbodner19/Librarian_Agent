# Librarian Agent — setup script
# Run from the project directory: .\install.ps1

$ProjectDir = $PSScriptRoot

# 1. Create virtual environment
Write-Host "Creating virtual environment..."
python -m venv "$ProjectDir\.venv"

# 2. Install dependencies
Write-Host "Installing dependencies..."
& "$ProjectDir\.venv\Scripts\pip.exe" install watchdog python-dotenv

# 3. Create logs folder
New-Item -ItemType Directory -Force -Path "$ProjectDir\logs" | Out-Null

# 4. Create .env from example if it doesn't exist
if (-not (Test-Path "$ProjectDir\.env")) {
    Copy-Item "$ProjectDir\.env.example" "$ProjectDir\.env"
    Write-Host ""
    Write-Host "Created .env from .env.example — edit it with your SOURCE_DIR and DEST_DIR before starting."
    Write-Host ""
}

# 5. Register scheduled task
Write-Host "Registering scheduled task..."
$action = New-ScheduledTaskAction `
    -Execute "$ProjectDir\.venv\Scripts\pythonw.exe" `
    -Argument "$ProjectDir\main.py" `
    -WorkingDirectory $ProjectDir
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -Hidden
Register-ScheduledTask -TaskName "LibrarianAgent" -Action $action -Trigger $trigger -Settings $settings -Force | Out-Null

Write-Host ""
Write-Host "Done. Edit .env then run: Start-ScheduledTask -TaskName 'LibrarianAgent'"
