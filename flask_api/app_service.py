import datetime
import pptxParser
import files_db
from tabels import Upload, Status,_session
from sql_db import sqldb

db = files_db.Filedb()

sql_db = sqldb()


def upload_pptx(pptx_file):
    """
       Uploads a PowerPoint file and saves the details in sql and the slides in file

       Parameters:
           pptx_file (FileStorage): The PowerPoint file to upload.

       Returns:
           int: The unique id associated with the uploaded presentation.

       Raises:
           ValueError: If the provided file is not a valid PowerPoint file.

       Example:
           id = upload_pptx(pptx_file)

       """
    presentation_as_list_of_slides = pptxParser.get_presentation_as_list_of_slides(pptx_file)

    upload = Upload(
        upload_time=datetime.datetime.now(),
        status=Status.pending,
        filename=pptx_file.filename
    )

    sql_db.add_Upload(upload)

    db.save(presentation_as_list_of_slides, upload.upload_path)

    return upload.id


def get_explanation_by_uid(uid):
    """
       Retrieve the explanation ready to download by unique identifier (UID).

       Args:
           uid (int): Unique identifier for the explanation.

       Returns:
           dict: A dictionary containing the UID, data, original name, and timestamp., or None if the UID doesn't exist.
       """
    upload = sql_db.get_Upload(uid)

    if not upload:
        return None

    upload_dict = upload.to_dict()
    upload_dict['slides'] = db.get(upload.upload_path)

    if upload.status != Status.pending:
        upload_dict['explain'] = db.get(upload.downloads_path)

    return upload_dict


