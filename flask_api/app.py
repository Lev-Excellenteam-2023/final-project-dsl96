from zipfile import BadZipFile

from flask import Flask, request, jsonify
import upload_pptx_service

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file found in request!', 400

    file = request.files['file']
    if file.filename == '':
        return 'No file selected!', 400

    try:
        uid = upload_pptx_service.upload_pptx(file)
    except (BadZipFile, ValueError) as e:
        error_message = str(e)
        return 'its not pptx file ' + error_message, 400

    response = {
        'msg': 'File saved successfully!',
        'UID': uid
    }
    return jsonify(response), 200


def run_api():
    app.run(debug=True)


if __name__ == '__main__':
    run_api()
