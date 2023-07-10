import logging
from zipfile import BadZipFile
from flask import Flask, request, jsonify
import app_service
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
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        error_msg = 'No file selected!'
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    try:
        uid = app_service.upload_pptx(file)
    except (BadZipFile, ValueError) as e:
        error_message = str(e)
        logging.error('Invalid file format: %s', error_message)
        return jsonify({'error_msg': 'Invalid file format: ' + error_message}), 400

    response = {
        'msg': 'File saved successfully!',
        'UID': uid
    }

    logging.info('File uploaded successfully with UID: %s', uid)
    return jsonify(response), 200


@app.route('/status', methods=['GET'])
def get_explanation():
    uid = int(request.args.get('uid'))

    if not uid:
        error_msg = 'Missing UID parameter'
        logging.error(error_msg)
        return jsonify({'error_msg': error_msg}), 400

    explanation_data = app_service.get_explanation_by_uid(uid)

    if not explanation_data:
        error_msg = 'not found'
        logging.error(error_msg)
        return jsonify({'status': error_msg}), 400

    return jsonify(explanation_data), 200


def run_api():
    app.run(debug=True)


if __name__ == '__main__':
    run_api()
