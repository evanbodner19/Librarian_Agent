# Librarian Agent

A file watcher that monitors your Downloads folder and automatically moves files to an external hard drive. If the drive isn't connected, files are held in a local queue and transferred automatically when the drive reconnects.

## What it does

- Watches `SOURCE_DIR` for new files
- Moves files to `DEST_DIR` on the external drive
- Skips temp files (`.crdownload`, `.part`, `.tmp`, `.temp`)
- Retries moves up to 3 times to handle browser-locked files
- Queues files locally if the drive is not connected, transfers them automatically when it reconnects
- Logs all transfers to `logs\drive_transfer.log`

## Tech stack

- Python 3.x
- [`watchdog`](https://github.com/gorakhargosh/watchdog) — filesystem event monitoring
- [`python-dotenv`](https://github.com/theskumar/python-dotenv) — environment variable config

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

4. Run:

   ```bash
   python main.py
   ```

## Project structure

```
Librarian_Agent/
├── main.py        # Watcher, queue, and transfer logic
├── .env           # Your local config (not committed)
├── .env.example   # Config template
├── queue/         # Temporary holding folder when drive is disconnected
└── logs/
    └── drive_transfer.log
```

## Configuration

Set these in your `.env` file:

| Variable | Description |
|---|---|
| `SOURCE_DIR` | Folder to watch (e.g. your Downloads folder) |
| `DEST_DIR` | Destination on the external drive (e.g. `E:\Sorted`) |

## Status

`external-drive` branch — raw transfer to external drive with offline queuing. Sorting logic will be added on merge with `main`.
