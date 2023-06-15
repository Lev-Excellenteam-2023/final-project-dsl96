import json
import os
import re
import uuid
from datetime import datetime
import file_system_db_util as util


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
        new_name, new_uid = util.generate_filename(name)
        new_path = os.path.join(self.UPLOAD_DIR, new_name)

        with open(new_path, 'w') as file:
            json.dump({
                'name': name,
                'slides': obj_to_save
            }, file)

        return new_uid

    def get_file_ready_to_download_by_uid(self, uid):
        all_ready_to_download_files_names = self.get_all_files_names(self.DOWNLOADS_DIR)
        file_name_start_with_uid = next(
            filter(lambda file_name: util.extract_data_from_file_name(file_name)[0] == uid, all_ready_to_download_files_names),
            None)

        if not file_name_start_with_uid:
            return None

        path = os.path.join(self.DOWNLOADS_DIR, file_name_start_with_uid)
        with open(path) as file:
            data = json.load(file)

        uid , timestamp, original_name = util.extract_data_from_file_name(file_name_start_with_uid)
        return {'uid':uid, 'explain': data, 'original name': original_name, 'timestamp': timestamp}

    def get_all_upload_files_uid(self):
        return [util.extract_data_from_file_name(fname)[0] for fname in self.get_all_files_names(self.UPLOAD_DIR)]

    def get_all_files_names(self, dir):
        return [entry.name for entry in os.scandir(dir) if entry.is_file()]


if __name__ == '__main__':
    db = Filedb()
    print(db.get_file_ready_to_download_by_uid('21ee163d-29dc-4c91-8c1a-b38b6a690664'))

    print(os.path.abspath(__file__))
