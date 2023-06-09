import os
class explainer_file_db():
    def __init__(self):
        # get dir to file folder (create if dont exist)
        root_dir = os.path.dirname(os.getcwd())
        self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
        self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)

    def get_all_upload_name(self):
        return [file for file in os.listdir(self.UPLOAD_DIR) if os.path.isfile(os.path.join(self.UPLOAD_DIR, file))]