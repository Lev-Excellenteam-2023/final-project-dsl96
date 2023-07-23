import time

import requests
import json
from datetime import datetime
from status import Status

import requests

class MyApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload_file(self, file_path, email=None):
        url = f"{self.base_url}/upload"
        files = {'file': open(file_path, 'rb')}
        data = {'email': email} if email else None

        try:
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            return Status(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error occurred during file upload: {e}")
            return None

    def status(self, id):
        url = f"{self.base_url}/status"
        params = {'id': id}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            return  Status(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while getting explanation by UID: {e}")
            return None

    def get_upload_by_mail_filename(self, email, filename):
        url = f"{self.base_url}/status"
        data = {'email': email, 'filename': filename}

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while getting upload by email and filename: {e}")
            return None


    def add_user(self, email):
        url = f"{self.base_url}/add_user"
        data = {'email': email}
        response = None  # Initialize response to None

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is not None and response.status_code >= 400:
                print(f"Error occurred while adding a user: {response.json().get('error_msg')}")
            else:
                print("Unknown error occurred during the API request.")
            return None

    def user_history(self, email):
        url = f"{self.base_url}/history"
        params = {'email': email}
        response = None
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4xx and 5xx status codes
            return [ Status(upload) for upload in response.json().get('uploads')]
        except requests.exceptions.RequestException as e:
                if response is not None and response.status_code >= 400:
                    print(f"Error occurred while adding a user: {response.json().get('error_msg')}")
                else:
                    print("Unknown error occurred during the API request.")
                return None




if __name__ == '__main__':
    client = MyApiClient('http://127.0.0.1:5000')
    r = client.user_history('dov315@gmail.com')



    print(r)
