from fastapi import File, UploadFile, Depends, status, HTTPException, APIRouter, BackgroundTasks
from app.schemas import schemas_file
from app.services.shared.repository import find_file_by_name
from database.database_engine import get_db
from config.settings import DOCLING_ALLOWED_TYPES
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger.log_conf import get_logger

from app.services.ingestion_pipeline import run_upload, background_ingestion_pipeline
from app.services.upload_file_logic import check_file_exists
from app.services.shared import find_file_by_id, get_all_files
from app.services.file_delete_logic import delete_file_from_db, delete_file_from_disc
logger = get_logger(__name__)

router = APIRouter(
    prefix="/file",
    tags=['Files']
)

@router.post("/upload_file", status_code=status.HTTP_201_CREATED)
async def upload_file_enpoint(background_tasks: BackgroundTasks, file: UploadFile=File(...), db: AsyncSession=Depends(get_db)):
    """

    Endpoint for upload files
    
    """
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No found file")

    if file.content_type not in DOCLING_ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"not allowed type")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing content")

    file_exists, file_content_hash = await check_file_exists(content, db)

    if file_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File |{file.filename}| exists")
    
    #upload checkpoint
    file_db_info, file_path = await run_upload(file=file,
                                         file_content_hash=file_content_hash, db=db)

    file_id = file_db_info.id 

    background_tasks.add_task(
        background_ingestion_pipeline,
        file_id=file_id,
        file_path=file_path
    )                                    
   
    
    
    return {f"file_id = {file_id}": file_db_info}
   
    
@router.get("/file_status/{file_id}", status_code=status.HTTP_200_OK ,response_model=schemas_file.FileResponse)
async def check_file_status(file_id: str, db:AsyncSession=Depends(get_db)):
    file =  await find_file_by_id(file_id=file_id, db=db)
    return file


@router.delete("/delete_file/{file_id}", status_code=status.HTTP_200_OK)
async def delete_file_endpoint(file_id: str, db: AsyncSession=Depends(get_db)):
    file = await find_file_by_id(file_id, db)
    
    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found file with id: {file_id}")

    await delete_file_from_disc(file)
    await delete_file_from_db(file, db)



    return {"message": f"File id: {file_id} has been deleted"}

@router.get("/find_file/{file_name}", status_code=status.HTTP_200_OK)
async def find_post_by_name_endpoint(file_name: str, db: AsyncSession=Depends(get_db)):
    file = await find_file_by_name(file_name, db)
    
    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found file with id: {file_name}")
    
    return file

@router.get("/all_files", status_code=status.HTTP_200_OK)
async def get_all_files_endpoint(db: AsyncSession=Depends(get_db)) -> list[schemas_file.FileResponse]:
    return await get_all_files(db)

@router.get("/delete_file/delete_all_files")
async def delete_all_files_endpoint(db: AsyncSession=Depends(get_db)):
    files_list = await get_all_files(db)

    for file in files_list:
        await delete_file_from_disc(file)
        await delete_file_from_db(file, db)
    
    return {"message": "files delete"}