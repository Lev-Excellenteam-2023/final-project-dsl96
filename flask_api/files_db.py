import json
import os
import re
import uuid
from datetime import datetime


class Filedb:
    def __init__(self):
        # get dir to file folder (create if dont exist)
        root_dir = os.path.dirname(os.getcwd())
        self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
        self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)

    def add(self, obj_to_save, name):
        """
          Add an object to be saved as a JSON file to 'uploads' folder

          Args: obj_to_save (object): The object to be saved as a JSON file. name (str): The name used for generating
          the filename.

          Returns:
              str: The unique ID associated with the saved file.(the finale name is 'unique_id_timestamp_original_name')
          """
        new_name, new_uid = self.generate_filename(name)
        new_path = os.path.join(self.UPLOAD_DIR, new_name)

        with open(new_path, 'w') as file:
            json.dump({
                'topic': name,
                'slides': obj_to_save
            }, file)

        return new_uid

    def get_file_ready_to_download_by_uid(self, uid):
        all_ready_to_download_files_names = self.get_all_files_names(self.DOWNLOADS_DIR)
        file_name_start_with_uid = next(
            filter(lambda file_name: self.get_uid_from_file_name(file_name) == uid, all_ready_to_download_files_names),
            None)

        if not file_name_start_with_uid:
            return None

        path = os.path.join(self.DOWNLOADS_DIR, file_name_start_with_uid)
        with open(path) as file:
            data = json.load(file)

        return data

    def get_uid_from_file_name(self, file_name):
        return re.search(r'([^_]+)_', file_name).group(1)

    def get_all_upload_files_uid(self):
        return [self.get_uid_from_file_name(fname) for fname in self.get_all_files_names(self.UPLOAD_DIR)]

    def get_all_files_names(self, dir):
        return [entry.name for entry in os.scandir(dir) if entry.is_file()]

    def generate_filename(self, original_name):
        """
          Generate a unique filename based on the original name.
          format 'unique-id_timestamp_original-name'

          Args:
              original_name (str): The original filename.

          Returns:
              tuple: A tuple containing the generated filename and unique ID.
          """
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("h%H_m%M_s%S")
        return unique_id + '_' + timestamp + '_' + original_name, unique_id


if __name__ == '__main__':
    db = Filedb()
    print(db.get_file_ready_to_download_by_uid('1686085676'))

    print(os.path.abspath(__file__))
