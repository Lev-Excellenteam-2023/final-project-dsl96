import pptxParser
import files_db
import util
db = files_db.Filedb()


def upload_pptx(pptx_file):
    """
       Uploads a PowerPoint file and saves the presentation slides to a upload file.
       the file will save with name format TIMESTAMP_UID_ORIGINAL_FILE-NAME(NO .pptx EXTENSION)

       Parameters:
           pptx_file (FileStorage): The PowerPoint file to upload.

       Returns:
           str: The unique identifier (UID) associated with the uploaded presentation.

       Raises:
           ValueError: If the provided file is not a valid PowerPoint file.

       Example:
           uid = upload_pptx(pptx_file)

       """
    presentation_as_list_of_slides = pptxParser.get_presentation_as_list_of_slides(pptx_file)
    file_name = util.get_file_name_without_extension(pptx_file.filename)

    uid = db.add(presentation_as_list_of_slides, file_name)

    return uid


def get_explanation_by_uid(uid):
    """
       Retrieve the explanation ready to download by unique identifier (UID).

       Args:
           uid (str): Unique identifier for the explanation.

       Returns:
          list[str] or None: The list of explanations associated with the given UID, or None if the UID dont ready
           to download or doesn't exist.

       """
    return db.get_file_ready_to_download_by_uid(uid)


def check_if_uid_exist(uid):
    return uid in db.get_all_upload_files_uid()
