
import uuid
import glob
import json
from datetime import datetime


# todo  add docs
def generate_filename(original_name, uid=None):
    if not uid:
        uid = str(uuid.uuid4())
    timestamp = datetime.now().strftime("h%H_m%M_s%S")
    return uid + '_' + timestamp + '_' + original_name, uid


def extract_uid_from_file_name(fname):
    split_parts = fname.split("_")
    uid = split_parts[0]
    return uid


def get_first_file_start_with(folder_path, start):
    file_pattern = folder_path + '\\' + start + "*"
    matching_files = glob.glob(file_pattern)

    if not matching_files:
        return None
    return matching_files[0]
