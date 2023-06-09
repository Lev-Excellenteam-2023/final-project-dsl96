
def __init__(self):
    # get dir to file folder (create if dont exist)
    root_dir = os.path.dirname(os.getcwd())
    self.UPLOAD_DIR = os.path.join(root_dir, 'files', 'uploads')
    self.DOWNLOADS_DIR = os.path.join(root_dir, 'files', 'download')
    os.makedirs(self.UPLOAD_DIR, exist_ok=True)
    os.makedirs(self.DOWNLOADS_DIR, exist_ok=True)