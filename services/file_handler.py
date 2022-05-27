from asyncio import constants
from os import scandir, mkdir, rename
from os.path import splitext, exists, dirname
from configs import folder_path, file_extensions
from watchdog.events import FileSystemEventHandler
import logging
from shutil import move


def init_folder(folder_paths):
    for folder_path in folder_paths:
        is_path_valid = exists(folder_path)
        if not is_path_valid:
            print(
                f"folder doesn't exist,automatically created one named {dirname(folder_path)}")
            mkdir(folder_path)


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(name)
        rename(entry, unique_name)
    move(entry, dest)


def make_unique(path):
    filename, extension = splitext(path)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1

    return path


class CategorizeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(folder_path.SOURCE_DIR_PATH) as entries:
            for entry in entries:
                name = entry.name

                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in file_extensions.audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                dest = folder_path.AUDIO_DIR_PATH
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in file_extensions.video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(folder_path.VIDEO_DIR_PATH, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in file_extensions.image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(folder_path.IMAGE_DIR_PATH, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in file_extensions.document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(folder_path.DOC_DIR_PATH, entry, name)
                logging.info(f"Moved document file: {name}")
