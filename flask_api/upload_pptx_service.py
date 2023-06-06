import pptxParser
import files_db
import util

db = files_db.Filedb()


def upload_pptx(pptx_file):
    """
       Uploads a PowerPoint file and saves the presentation slides to a upload file.
       the file will save with name format TIMESTAMP-UID-ORIGINAL_FILE_NAME(NO .pptx EXTENSION)

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
