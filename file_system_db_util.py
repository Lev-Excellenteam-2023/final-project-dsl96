import uuid
from datetime import datetime

def generate_uid_timestamp_name(name):
    uid = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{uid}_{timestamp}_{name}"