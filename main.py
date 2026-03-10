import time
import os
import shutil
import logging
import threading
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from extension_map import EXTENSION_MAP

load_dotenv()

SOURCE_DIR = os.getenv("SOURCE_DIR")
DEST_DIR = os.getenv("DEST_DIR")
QUEUE_DIR = "queue"
TEMP_EXTENSIONS = {".crdownload", ".part", ".tmp", ".temp"}

# Invert EXTENSION_MAP for O(1) lookups: extension → category
LOOKUP = {}
for category, extensions in EXTENSION_MAP.items():
    for ext in extensions:
        LOOKUP[ext] = category

# --- Queue Logic ---

def add_to_queue(file_path):
    os.makedirs(QUEUE_DIR, exist_ok=True)

    if os.path.dirname(os.path.abspath(file_path)) == os.path.abspath(QUEUE_DIR):
        return

    for attempt in range(3):
        try:
            queue_path = os.path.join(QUEUE_DIR, os.path.basename(file_path))
            shutil.move(file_path, queue_path)
            logging.info(f"Added to queue: {file_path} -> {queue_path}")
            break
        except Exception as e:
            if attempt < 2:
                logging.warning(f"Attempt {attempt + 1} failed to queue {os.path.basename(file_path)} due to {e}")
                time.sleep(1)
            else:
                logging.error(f"Failed to queue {os.path.basename(file_path)} after 3 attempts, skipping due to {e}")

def process_queue():
    os.makedirs(QUEUE_DIR, exist_ok=True)
    files = [f for f in os.listdir(QUEUE_DIR) if os.path.isfile(os.path.join(QUEUE_DIR, f))]

    if not files:
        return

    for file in files:
        queue_path = os.path.join(QUEUE_DIR, file)
        transfer_file(queue_path)

# --- File Transfer Logic ---

def transfer_file(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in TEMP_EXTENSIONS:
        return

    drive, _ = os.path.splitdrive(DEST_DIR)
    if not os.path.exists(drive):
        add_to_queue(file_path)
        return

    category = LOOKUP.get(ext, 'Other')
    dest_dir = os.path.join(DEST_DIR, category)
    os.makedirs(dest_dir, exist_ok=True)

    dest = os.path.join(dest_dir, os.path.basename(file_path))
    for attempt in range(3):
        try:
            shutil.move(file_path, dest)
            logging.info(f"Moved: {file_path} to {dest}")
            break
        except Exception as e:
            if attempt < 2:
                logging.warning(f"Attempt {attempt + 1} failed to move {os.path.basename(file_path)} due to {e}")
                time.sleep(1)
            else:
                logging.error(f"Failed to move {os.path.basename(file_path)} after 3 attempts, skipping due to {e}")

# --- Event Handler ---
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            transfer_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            transfer_file(event.dest_path)

# --- Drive Polling ---
def poll_drive():
    while True:
        time.sleep(5)
        drive, _ = os.path.splitdrive(DEST_DIR)
        if os.path.exists(drive):
            process_queue()

if __name__ == "__main__":
    logging.basicConfig(filename=r'logs\librarian.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    threading.Thread(target=poll_drive, daemon=True).start()
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()
    logging.info(f"Watching {SOURCE_DIR}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
