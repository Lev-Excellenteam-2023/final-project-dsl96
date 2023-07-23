import datetime
import pptxParser
import files_db
from tabels import Upload, Status, _session, User
from sql_db import sqldb

file_db = files_db.Filedb()

sql_db = sqldb()


def upload_pptx(pptx_file, user_email=None):
    """
    Uploads a PowerPoint (.pptx) file and associates it with a user in the database.

    Parameters
    ----------
    pptx_file : File object
        The PowerPoint (.pptx) file to be uploaded.

    user_email : str, optional
        The email of the user to whom the uploaded file should be associated.
        If not provided (None), the file will be associated with no specific user.

    Returns
    -------
    Upload
        The Upload object representing the uploaded PowerPoint file.

    Raises
    ------
    ValueError
        If the provided user_email is not associated with any existing user.
    """
    presentation_as_list_of_slides = pptxParser.get_presentation_as_list_of_slides(pptx_file)

    upload = Upload(
        upload_time=datetime.datetime.now(),
        status=Status.pending,
        filename=pptx_file.filename
    )

    if user_email:
        sql_db.add_upload_to_user_by_email(upload=upload, email=user_email)
    else:
        sql_db.add_Upload(upload)

    file_db.save(presentation_as_list_of_slides, upload.upload_path)

    return make_response_dict_from_upload(upload)



def get_latest_upload_by_filename(uploads, filename):
    """
          Retrieve  list of uploads.

          Args:
              uploads: Unique list of uploads .
              filename (str):name of the original upload file

          Returns:
               uploads: return the latest upload with the name filename.
          """
    uploads_filter_by_filename = [upload for upload in uploads if upload.filename == filename]

    if uploads_filter_by_filename:
        earliest_upload = min(uploads_filter_by_filename, key=lambda upload: upload.upload_time)
        return earliest_upload
    else:
        return None


def get_upload_by_mail_filename(email, filename):
    user = sql_db.get_user_by_email(email)

    if not user:
        raise ValueError(f'user email{email} dont exist')
    upload = get_latest_upload_by_filename(user.uploads, filename)

    if not upload:
        raise ValueError(f'user email{email} dont hav {filename}')

    return make_response_dict_from_upload(upload)


def make_response_dict_from_upload(upload):
    """
          return dict ready to response.

          Args:
              upload  :upload object

          Returns:
              dict: A dictionary containing  upload data and also the slides and explanetion .
          """
    upload_dict = upload.to_dict()
    upload_dict['slides'] = file_db.get(upload.upload_path)

    if upload.status != Status.pending:
        upload_dict['explain'] = file_db.get(upload.downloads_path)

    return upload_dict


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
        raise ValueError(f'uid dont exist')

    return make_response_dict_from_upload(upload)


def create_user(*, email):
    user = User(email=email)
    sql_db.add_user(user)
    return user


def get_user(*, email):
    user = sql_db.get_user_by_email(email)
    if not user:
        raise ValueError(f'user dont exist')
    return user.to_dict()


if __name__ == '__main__':
    file_db = sqldb()


    u =  get_user(email='206tamar@gmail.com')
    print(u)
