import time
import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE_DIR = r"C:\Users\EvBod\Downloads"
DEST_DIR = r"O:\Sorted"
TEMP_EXTENSIONS = {".crdownload", ".part", ".tmp", ".temp"}

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self._transfer(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._transfer(event.dest_path)

    def _transfer(self, file_path):
        _, ext = os.path.splitext(file_path)
        if ext.lower() in TEMP_EXTENSIONS:
            return
        
        drive, _ = os.path.splitdrive(DEST_DIR)
        if not os.path.exists(drive):
            logging.warning(f"Drive not found: {drive}, skipping file: {os.path.basename(file_path)}")
            return
        
        os.makedirs(DEST_DIR, exist_ok=True)
        
        dest = os.path.join(DEST_DIR, os.path.basename(file_path))
        for attempt in range(3):
            try:
                shutil.move(file_path, dest)
                logging.info(f"Moved: {file_path} to {dest}")
                break
            except Exception as e:
                if attempt < 2:
                    logging.warning(f"Attempt {attempt + 1} failed to move {file_path} due to {e}")
                    time.sleep(2)
                else:
                    logging.error(f"Failed to move {file_path} after 3 attempts, skipping due to {e}")


if __name__ == "__main__":
    logging.basicConfig(filename=r'logs\drive_transfer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()