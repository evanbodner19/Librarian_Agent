# Librarian Agent

A file watcher that monitors your Downloads folder and automatically moves files to an external hard drive.

## What it does

- Watches `SOURCE_DIR` for new files
- Moves files to `DEST_DIR` on the external drive
- Skips temp files (`.crdownload`, `.part`, `.tmp`, `.temp`)
- Retries moves up to 3 times to handle browser-locked files
- Logs all transfers to `logs\drive_transfer.log`
- Handles drive-not-connected gracefully — logs a warning and skips

## Tech stack

- Python 3.x
- [`watchdog`](https://github.com/gorakhargosh/watchdog) — filesystem event monitoring

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install watchdog
   ```

3. Run:

   ```bash
   python main.py
   ```

## Project structure

```
Librarian_Agent/
├── main.py       # Watches Downloads and moves files to external drive
└── logs/
    └── drive_transfer.log
```

## Configuration

Paths are hardcoded in `main.py`:

| Variable | Description |
|---|---|
| `SOURCE_DIR` | Folder to watch (e.g. your Downloads folder) |
| `DEST_DIR` | Destination on the external drive (e.g. `O:\Sorted`) |

## Status

`external-drive` branch — raw transfer to external drive, no sorting logic yet. Sorting will be added on merge with `main`.
