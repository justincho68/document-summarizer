import os
import uuid
from fastapi import UploadFile
from pathlib import Path

#upload directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

#takes in UploadFile which is fastAPI class
async def save_upload_file(upload_file: UploadFile) -> str:
    #generate unique filename for each file
    #splits the file from the name and the extension 
    file_extension = os.path.splitext(upload_file.filename)[1].lower()
    #uuid to create unique file name 
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        #reads entire block asynchronously and is non-blocking
        content = await upload_file.read()
        buffer.write(content)
    #full path to newly saved file 
    #should be in form uploads/unique id .pdf
    return str(file_path)

def clean_up_file(file_path: str) -> None:
    try:
        #attempt OS level file system delete
        os.remove(file_path)
    except Exception as e:
        print(f"Error removing file {file_path}: {e}")