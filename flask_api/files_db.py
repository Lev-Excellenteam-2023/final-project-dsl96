import os
import time
import uuid
import json


class Filedb:
    def __init__(self):
        # Get the current directory
        current_dir = os.getcwd()
        # Get the parent directory
        parent_dir = os.path.dirname(current_dir)

        self.UPLOAD_DIR = os.path.join(parent_dir, 'files', 'uploads')
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    def add(self, obj_to_save, name):
        new_name, new_uid = self.generate_filename(name)
        new_path = os.path.join(self.UPLOAD_DIR, new_name)

        with open(new_path, 'w') as file:
            json.dump(obj_to_save, file)

        return new_uid

    def generate_filename(self, original_filename):
        unique_id = str(uuid.uuid4())
        timestamp = str(int(time.time()))
        return timestamp + '_' + unique_id + '_' + original_filename, unique_id
