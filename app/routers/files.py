from fastapi import File, UploadFile, Depends, status, HTTPException, APIRouter
from app.services import upload_file_logic
from app.schemas import schemas_file
from database import models
from database.database_engine import get_db
from config.settings import ALLOWED_TYPES

from sqlalchemy.orm import Session




router = APIRouter(
    prefix="/file",
    tags=['Files']
)

@router.post("/upload_file", status_code=status.HTTP_201_CREATED, response_model=schemas_file.FileResponse)
async def upload_file_enpoint(file: UploadFile=File(...), db: Session=Depends(get_db)):
    """

    Endpoint for upload files
    
    """
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No found file")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"not allowed type")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing content")
    
    file_exists, file_content_hash = upload_file_logic.check_file_exists(content, db)

    if file_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File |{file.filename}| exists")
    
    file_path = await upload_file_logic.save_file_on_disc(file_object=file, file_content_hash=file_content_hash)

    file_info = upload_file_logic.add_file_to_database(file_name=file.filename,
                                           file_content_hash=file_content_hash,
                                           file_size=file.size,
                                           file_content_type=file.content_type,
                                           file_path=file_path, db=db)

    return file_info