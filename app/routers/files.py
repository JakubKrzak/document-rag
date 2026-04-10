from fastapi import File, UploadFile, Depends, status, HTTPException, APIRouter

import asyncio, shutil
from app import hash_content

from sqlalchemy.orm import Session

from database.database_engine import get_db
from database import models

from schemas import schemas_file


router = APIRouter(
    prefix="/file",
    tags=['Files']
)

@router.post("/upload_file", status_code=status.HTTP_201_CREATED, response_model=schemas_file.FileResponse)
async def upload_file(file: UploadFile=File(...), db: Session=Depends(get_db)):
    """

    Endpoint for upload files
    
    """
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No found file")

    content = await file.read()
    current_hashed_content = hash_content.hash_file_content(content)

    existing_file = db.query(models.File).filter(models.File.hashed_content == current_hashed_content).first()

    if existing_file:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File |{file.filename}| exists")
    
    file_path = f"disc/{file.filename}_{current_hashed_content[:8]}"

    file.file.seek(0)
    with open(file_path, "wb") as buffor:
        await asyncio.to_thread(shutil.copyfileobj, file.file, buffor)

    new_file = models.File(file_name=file.filename,
                           hashed_content=current_hashed_content,
                           file_size=file.size,
                           file_type=file.content_type,
                           file_path=file_path)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file