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
- [NSSM](https://nssm.cc) — runs the script as a named Windows service

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install watchdog python-dotenv
   ```

3. Copy `.env.example` to `.env` and fill in your paths:

   ```bash
   cp .env.example .env
   ```

4. Run directly:

   ```bash
   python main.py
   ```

   Stop with `Ctrl+C`.

## Running as a Windows service

Install [NSSM](https://nssm.cc/download) then run as Administrator:

```powershell
nssm install LibrarianAgent
```

In the GUI:
- **Path:** `<project_dir>\.venv\Scripts\python.exe`
- **Startup directory:** `<project_dir>`
- **Arguments:** `main.py`
- **I/O → Stdout/Stderr:** `<project_dir>\logs\librarian.log`

```powershell
nssm set LibrarianAgent AppEnvironmentExtra PYTHONUNBUFFERED=1
nssm set LibrarianAgent DisplayName "Librarian Agent"
nssm set LibrarianAgent Description "Watches Downloads folder and sorts files automatically"
nssm start LibrarianAgent
```

**Useful commands:**
```powershell
nssm restart LibrarianAgent
nssm stop LibrarianAgent
nssm status LibrarianAgent
Get-Content logs\librarian.log -Wait
```

Find the service under Task Manager → **Services tab**.

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

MVP — rule-based sorting to external drive with offline queue. Running as a Windows service.
