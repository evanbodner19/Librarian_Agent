# Librarian Agent

A file watcher that monitors your Downloads folder and automatically sorts files into subfolders based on file type. Runs as a Windows background service.

## What it does

- Watches a source folder (e.g. `Downloads`) for new files
- Sorts files into destination subfolders based on extension rules defined in `extension_map.py`
- Moves files automatically using `shutil.move()`
- Retries moves automatically if a file is still locked by another process
- Logs every move to a file via NSSM

## Tech stack

- Python 3.x
- [`watchdog`](https://github.com/gorakhargosh/watchdog) — filesystem event monitoring
- [NSSM](https://nssm.cc) — runs the script as a named Windows service

## Setup

1. Install the dependency:

   ```powershell
   pip install watchdog
   ```

2. Update the paths at the top of `main.py`:

   ```python
   SOURCE_DIR = r"C:\Users\you\Downloads"
   DEST_DIR   = r"C:\Users\you\Downloads\Sorted"
   ```

3. Add any additional file types to `extension_map.py` as needed.

4. Run directly:

   ```powershell
   python main.py
   ```

   Stop with `Ctrl+C`.

## Running as a Windows service

Install [NSSM](https://nssm.cc/download) then run as Administrator:

```powershell
winget install nssm
nssm install LibrarianAgent
```

In the GUI:
- **Path:** `C:\Users\you\AppData\Local\Programs\Python\Python312\python.exe`
- **Startup directory:** `C:\Users\you\Projects\Librarian_Agent`
- **Arguments:** `main.py`
- **I/O → Stdout/Stderr:** `C:\Users\you\Projects\Librarian_Agent\logs\librarian.log`

```powershell
nssm set LibrarianAgent AppEnvironmentExtra PYTHONUNBUFFERED=1
nssm set LibrarianAgent DisplayName "Librarian Agent"
nssm set LibrarianAgent Description "Watches Downloads folder and sorts files automatically"
nssm start LibrarianAgent
```

**Useful commands:**
```powershell
nssm restart LibrarianAgent   # pick up code changes
nssm stop LibrarianAgent
nssm status LibrarianAgent
```

**Watch logs live:**
```powershell
Get-Content C:\Users\you\Projects\Librarian_Agent\logs\librarian.log -Wait
```

Find the service under Task Manager → **Services tab**.

## Project structure

```
Librarian_Agent/
├── main.py           # Watcher, event handler, and sorting logic
├── extension_map.py  # File extension to category mapping
├── logs/             # Runtime logs (not committed)
└── .gitignore
```

## Next steps

Replace rule-based sorting with local AI classification using [Ollama](https://ollama.com) (llama3):

- A `classifier.py` module will send file metadata to a local llama3 model via the `ollama` Python SDK
- The model returns a category, replacing the static extension lookup
- Runs fully offline — no API keys required

## Status

MVP — rule-based sorting, running as a Windows service.
