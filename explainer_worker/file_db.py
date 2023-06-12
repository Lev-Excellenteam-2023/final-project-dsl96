import datetime
import os
import json
import string


class explainer_file_db():
    def __init__(self):
        # get dir to file folder (create if dont exist)
        root_dir = os.path.dirname(os.getcwd())
        self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
        self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)

    def get_all_upload_name(self):
        return [self.extract_uid_from_file_name(file) for file in os.listdir(self.UPLOAD_DIR) if os.path.isfile(os.path.join(self.UPLOAD_DIR, file))]

    def save_to_download(self, obj, uid, name):

        if not name.endswith(".json"):
            name += '.json'

        new_name = self.generate_uid_timestamp_name(self, uid, name)

        with open(self.DOWNLOADS_DIR + '\\' + new_name, 'w') as file:
            # Convert the object to a JSON string and write it to the file
            json.dump(obj, file)

    def extract_uid_from_file_name(self, fname):
        split_parts = fname.split("_")
        uid = split_parts[0]
        return uid


if __name__ == '__main__':
    db = explainer_file_db()
    n =  db.get_all_upload_name()
    print(n)
