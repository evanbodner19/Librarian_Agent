# Librarian Agent

A file watcher that monitors your Downloads folder and automatically sorts files to an external hard drive based on file type and extension rules.

## What it does

- Watches a source folder (e.g. `Downloads`) for new files
- Sorts files into destination subfolders based on extension/type rules
- Moves files to an external drive automatically
- Tracks state to avoid reprocessing files

## Tech stack

- Python 3.x
- [`watchdog`](https://github.com/gorakhargosh/watchdog) — filesystem event monitoring
- `python-dotenv` — environment variable management

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```   WATCH_FOLDER=C:/Users/you/Downloads
   DEST_ROOT=E:/Sorted
   ```

4. Run:

   ```bash
   python main.py
   ```

## Project structure

```Librarian_Agent/
├── main.py           # Entry point, starts the file watcher
├── sorter.py         # Rule-based file categorization by extension
├── mover.py          # File move logic
├── config.py         # Path and category configuration
├── requirements.txt
├── .env              # Not committed
└── .gitignore
```

## Configuration

| Variable | Description |
|---|---|
| `WATCH_FOLDER` | Folder to monitor (default: `~/Downloads`) |
| `DEST_ROOT` | Root of destination drive/folder |

## Next steps

Replace rule-based sorting with local AI classification using [Ollama](https://ollama.com) (llama3):

- `classifier.py` will send file metadata (name, extension, size) to a local llama3 model via the `ollama` Python SDK
- The model returns a category, replacing the static extension lookup in `sorter.py`
- Adds `OLLAMA_MODEL` and `OLLAMA_HOST` config vars
- Runs fully offline — no API keys required

## Status

MVP — rule-based sorting.
