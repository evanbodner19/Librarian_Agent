# Librarian Agent

A file watcher that monitors your Downloads folder and automatically sorts files into subfolders based on file type.

## What it does

- Watches a source folder (e.g. `Downloads`) for new files
- Sorts files into destination subfolders based on extension rules defined in `extension_map.py`
- Moves files automatically using `shutil.move()`
- Prints a log of every move to the console

## Tech stack

- Python 3.x
- [`watchdog`](https://github.com/gorakhargosh/watchdog) — filesystem event monitoring

## Setup

1. Install the dependency:

   ```bash
   pip install watchdog
   ```

2. Update the paths at the top of `main.py`:

   ```python
   SOURCE_DIR = r"C:\Users\you\Downloads"
   DEST_DIR   = r"C:\Users\you\Downloads\Sorted"
   ```

3. Add any additional file types to `extension_map.py` as needed.

4. Run:

   ```bash
   python main.py
   ```

   Stop with `Ctrl+C`.

## Project structure

```
Librarian_Agent/
├── main.py           # Watcher, event handler, and sorting logic
├── extension_map.py  # Matching dictionary for file extensions
└── .gitignore
```

## Next steps

Replace rule-based sorting with local AI classification using [Ollama](https://ollama.com) (llama3):

- A `classifier.py` module will send file metadata to a local llama3 model via the `ollama` Python SDK
- The model returns a category, replacing the static extension lookup
- Runs fully offline — no API keys required

## Status

MVP — rule-based sorting.
