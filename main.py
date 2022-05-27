import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from configs import folder_path

from services import file_handler


default_folders = [folder_path.IMAGE_DIR_PATH,
                   folder_path.DOC_DIR_PATH,
                   folder_path.AUDIO_DIR_PATH,
                   folder_path.VIDEO_DIR_PATH]

file_handler.init_folder(default_folders)


target_path = sys.argv[1] if len(sys.argv) > 1 else folder_path.SOURCE_DIR_PATH
print(f"setting source path: {target_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = target_path
    event_handler = file_handler.CategorizeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
