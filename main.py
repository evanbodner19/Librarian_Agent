import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from extension_map import EXTENSION_MAP

# Define source and destination directories (update these paths as needed)
SOURCE_DIR = r"C:\Users\EvBod\Downloads"
DEST_DIR = r"C:\Users\EvBod\Downloads\Sorted"


# Create a lookup dictionary for quick extension to category mapping from the EXTENSION_MAP
LOOKUP = {}
for category, extensions in EXTENSION_MAP.items():
    for ext in extensions:
        LOOKUP[ext] = category

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:          # Ignore new directories, return early
            return
        
        # Get the file path and extension
        file_path = event.src_path
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()               # Normalize the extension to lowercase


        # Determine the category based on the extension, default to 'Other' if not found
        subdir = LOOKUP.get(ext, 'Other')
        
        
        filename = os.path.basename(file_path)
        subdir_path = os.path.join(DEST_DIR, subdir)
        dest_path = os.path.join(DEST_DIR, subdir, filename)

        # Ensure the destination subdirectory exists
        os.makedirs(subdir_path, exist_ok=True)

        # Move the file to the appropriate subdirectory
        MAX_RETRIES = 3
        RETRY_DELAY = 2

        for attempt in range(MAX_RETRIES):
            time.sleep(RETRY_DELAY)  # Wait before retrying
            try:
                shutil.move(file_path, dest_path)
                print(f"Moved: {file_path} to {dest_path}")
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Error moving {file_path} to {dest_path}: {e}")


if __name__ == "__main__":
    librarian = FileHandler()
    observer = Observer()
    observer.schedule(librarian, SOURCE_DIR, recursive=False)
    observer.start()
    print(f"Monitoring {SOURCE_DIR} for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()