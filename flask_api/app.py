import logging
import sqlite3
from zipfile import BadZipFile
from flask import Flask, request, jsonify
import app_service
from sqlalchemy.exc import IntegrityError
from tabels import Status

app = Flask(__name__)

# Configure the logger
logging.basicConfig(level=logging.DEBUG)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Log request details
    log_message = f"Request Details: Method={request.method}, URL={request.url}, IP={request.remote_addr}, User-Agent={request.user_agent}"
    logging.info(log_message)

    # check if file send
    if 'file' not in request.files:
        error_msg = 'No file found in request!'
        return return_error_and_log(error_msg)

    file = request.files['file']
    email = request.form.get('email', None)

    # Check if a file is selected
    if file.filename == '':
        error_msg = 'No file selected!'
        return return_error_and_log(error_msg)

    try:
        upload = app_service.upload_pptx(file, user_email=email)
    except (BadZipFile, ValueError) as e:
        error_message = str(e)
        return return_error_and_log(error_message)

    logging.info('File uploaded successfully with UID: %s', upload['id'])
    return jsonify(upload), 200


@app.route('/status', methods=['GET'])
def get_explanation_by_uid():
    id = request.args.get('id', None)

    if not id:
        error_msg = 'Missing UID parameter'
        return return_error_and_log(error_msg)
    try:
        upload_data = app_service.get_explanation_by_uid(int(id))
    except ValueError as e:
        error_message = str(e)
        return return_error_and_log(error_message)

    return jsonify(upload_data), 200


@app.route('/status', methods=['POST'])
def get_upload_by_mail_filename():
    email = request.form.get('email', None)
    filename = request.form.get('filename', None)

    if not email or not filename:
        error_msg = 'Missing filename or email'
        return return_error_and_log(error_msg)
    try:
        upload_data = app_service.get_upload_by_mail_filename(email=email, filename=filename)
    except ValueError as e:
        error_message = str(e)
        return return_error_and_log(error_message)

    return jsonify(upload_data), 200


@app.route('/add_user', methods=['POST'])
def add_user():
    email = request.form.get('email')

    if not email:
        return jsonify({'error': 'Email not provided'}), 400

    try:
        new_user = app_service.create_user(email=email)
    except (ValueError,) as e:
        # email format or email dont exist
        error_message = str(e)
        return return_error_and_log(error_message)

    except IntegrityError as e:
        error_message = str(e)
        return return_error_and_log('email already exist' + error_message)

    return jsonify(new_user.to_dict()), 200


@app.route('/history', methods=['GET'])
def user_history():
    email = request.args.get('email')

    if not email:
        return return_error_and_log('missing email ergument')

    try:
        return app_service.get_user(email=email)
    except ValueError as e:
        # user dont exist
        error_message = str(e)
        return return_error_and_log(error_message)


def return_error_and_log(error_msg):
    logging.error(error_msg)
    return jsonify({'error_msg': error_msg}), 400


def run_api():
    app.run(debug=True)


if __name__ == '__main__':
    run_api()
