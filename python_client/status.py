import json


class Status:
    def __init__(self, data_dict):
        self.filename = data_dict.get('filename')
        self.finish_time = data_dict.get('finish_time')
        self.id = data_dict.get('id')
        self.slides = data_dict.get('slides',None)
        self.status = data_dict.get('status')
        self.uid = data_dict.get('uid')
        self.upload_time = data_dict.get('upload_time')
        self.user_id = data_dict.get('user_id')
        self.explain = data_dict.get('user_id', None)

    def is_done(self):
        return self.status == 'complete'

    def __repr__(self):
        return f"Status:\n" \
               f"id: {self.id}\n" \
               f"uid: {self.uid}\n" \
               f"Status: {self.status}\n" \
               f"Filename: {self.filename}\n" \
               f"Timestamp: {self.upload_time}\n" \
               f"Slides: {self.slides}\n"\
               f"explain: {self.explain}"