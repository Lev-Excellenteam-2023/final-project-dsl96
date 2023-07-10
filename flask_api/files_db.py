import json
import os
import file_system_db_util as util


class Filedb:
    def __init__(self):
        # get dir to file folder (create if dont exist)
        root_dir = os.path.dirname(os.getcwd())
      #  self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
       # self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
        self.SAVE_DIR = os.path.join(root_dir, 'files' )
      #  os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.SAVE_DIR, exist_ok=True)
       #

    def save(self, obj, name):
        file_path = os.path.join(self.SAVE_DIR, name + '.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(obj, file)

    def get(self, name):

        file_path = os.path.join(self.SAVE_DIR, name + '.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'r') as file:
            return json.load(file)







if __name__ == '__main__':
    db = Filedb()
    print(db.get_from_download('21ee163d-29dc-4c91-8c1a-b38b6a690664'))

    print(os.path.abspath(__file__))
