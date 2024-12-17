from fastapi import APIRouter, UploadFile, File
from app.utils.minio_utils import upload_file_to_minio

router = APIRouter()

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file to MinIO.
    """
    file_location = f"/tmp/{file.filename}"  # Save the file temporarily
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    
    # Upload the file to MinIO
    upload_file_to_minio(file_location, file.filename)
    
    return {"message": f"File '{file.filename}' uploaded successfully"}
