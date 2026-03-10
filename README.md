# Librarian Agent

A file watcher that monitors your Downloads folder, sorts files by type, and moves them to an external hard drive. If the drive isn't connected, files are held in a local queue and transferred automatically when it reconnects. Runs as a Windows background service.

## What it does

- Watches `SOURCE_DIR` for new files
- Sorts files into `DEST_DIR/<category>/` based on extension rules in `extension_map.py`
- Skips temp files (`.crdownload`, `.part`, `.tmp`, `.temp`)
- Retries moves up to 3 times to handle browser-locked files
- Queues files locally if the drive is not connected, transfers automatically when it reconnects
- Logs all activity to `logs/librarian.log`

## Tech stack

- Python 3.x
- [`watchdog`](https://github.com/gorakhargosh/watchdog) — filesystem event monitoring
- [`python-dotenv`](https://github.com/theskumar/python-dotenv) — environment variable config
- Windows Task Scheduler — runs the script automatically on login

## Setup

Run the install script from PowerShell (handles venv, dependencies, and task registration):

```powershell
.\install.ps1
```

Then edit `.env` with your paths and start the task:

```powershell
Start-ScheduledTask -TaskName "LibrarianAgent"
```

**Or manually:**

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install watchdog python-dotenv
   ```

2. Copy `.env.example` to `.env` and fill in your paths.

3. Run directly:

   ```bash
   python main.py
   ```

   Stop with `Ctrl+C`.

## Running as a background task

Register it with Windows Task Scheduler (runs automatically on login, no console window):

```powershell
$action = New-ScheduledTaskAction -Execute "<project_dir>\.venv\Scripts\pythonw.exe" -Argument "<project_dir>\main.py" -WorkingDirectory "<project_dir>"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -Hidden
Register-ScheduledTask -TaskName "LibrarianAgent" -Action $action -Trigger $trigger -Settings $settings -Force
```

Replace `<project_dir>` with your actual project path.

**Useful commands:**
```powershell
Start-ScheduledTask -TaskName "LibrarianAgent"
Stop-ScheduledTask -TaskName "LibrarianAgent"
Get-ScheduledTask -TaskName "LibrarianAgent"   # check status
Get-Content logs\librarian.log -Wait           # tail logs
```

Find the task under Task Scheduler → **Task Scheduler Library**.

## Project structure

```
Librarian_Agent/
├── main.py           # Watcher, queue, and transfer logic
├── extension_map.py  # File extension to category mapping
├── .env              # Your local config (not committed)
├── .env.example      # Config template
├── queue/            # Temporary holding folder when drive is disconnected
└── logs/
    └── librarian.log
```

## Configuration

Set these in your `.env` file:

| Variable | Description |
|---|---|
| `SOURCE_DIR` | Folder to watch (e.g. your Downloads folder) |
| `DEST_DIR` | Destination on the external drive (e.g. `E:\Sorted`) |

## Status

MVP — rule-based sorting to external drive with offline queue. Runs as a Windows scheduled task on login.
