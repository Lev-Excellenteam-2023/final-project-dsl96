import datetime
import os
import json
import string
import file_system_db_util as util


class explainer_file_db():
    def __init__(self):
        # get dir to file folder (create if dont exist)
        root_dir = os.path.dirname(os.getcwd())
        self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
        self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)

    def get_all_upload_uid(self):
        return [util.extract_uid_from_file_name(file) for file in os.listdir(self.UPLOAD_DIR) if os.path.isfile(os.path.join(self.UPLOAD_DIR, file))]
    def get_all_dowload_uid(self):
        return [util.extract_uid_from_file_name(file) for file in os.listdir(self.DOWNLOADS_DIR) if os.path.isfile(os.path.join(self.UPLOAD_DIR, file))]


    def save_to_download(self, obj, uid, name):

        if not name.endswith(".json"):
            name += '.json'

        new_name,uid = util.generate_filename(name, uid)

        with open(self.DOWNLOADS_DIR + '\\' + new_name, 'w') as file:
            # Convert the object to a JSON string and write it to the file
            json.dump(obj, file)
        return uid

    def get_from_download(self, uid):

        file_path = util.get_first_file_start_with(self.DOWNLOADS_DIR, uid)

        if not file_path:
            return None

        with open(file_path, 'r') as file:
            data = json.load(file)

        return data

    def get_from_uploads(self, uid):

        file_path = util.get_first_file_start_with(self.UPLOAD_DIR, uid)

        if not file_path:
            return None

        with open(file_path, 'r') as file:
            data = json.load(file)

        return data







if __name__ == '__main__':
    db = explainer_file_db()
    n =  db.get_all_upload_name()
    print(n)
