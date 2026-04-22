from fastapi import File, UploadFile, Depends, status, HTTPException, APIRouter
from app.services import file_delete_logic, upload_file_logic, file_services , file_parsed_content, file_chunk
from app.services.file_services import update_file_status
from app.schemas import schemas_file
from database.database_engine import get_db
from config.settings import DOCLING_ALLOWED_TYPES
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger.log_conf import get_logger
from database.models import FileStatus
logger = get_logger(__name__)

router = APIRouter(
    prefix="/file",
    tags=['Files']
)

@router.post("/upload_file", status_code=status.HTTP_201_CREATED, response_model=schemas_file.FileResponse)
async def upload_file_enpoint(file: UploadFile=File(...), db: AsyncSession=Depends(get_db)):
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

    file_exists, file_content_hash = await upload_file_logic.check_file_exists(content, db)

    if file_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File |{file.filename}| exists")
    
    
    """
    
    UPLOADED checkpoint:
    
        saving file on disc
        add file to database
        updated file status to UPLOADED
    
    """
    # Save file on disc
    file_path = await upload_file_logic.save_file_on_disc(file_object=file, file_content_hash=file_content_hash)
    # Add file info to db
    file_db_info = await upload_file_logic.add_file_to_database(file_name=file.filename,
                                                        file_content_hash=file_content_hash,
                                                        file_size=file.size,
                                                        file_content_type=file.content_type,
                                                        file_path=file_path,
                                                        status=FileStatus.UPLOADED,
                                                        db=db)
    file_id = file_db_info.id

    

    """
    
    PARSED checkpoint:

        parsed file content
        saving parsed file content on disc

    """

    parsed_object = await file_parsed_content.parsed_file_content(file_path=file_path)
    parsed_file_path = await file_parsed_content.save_parsed_file_on_disc(parsed_file=parsed_object)
    await file_services.add_parsed_info_to_db(file_id=file_id,
                                        parsed_file_path=parsed_file_path,
                                        pages=len(parsed_object.pages),
                                        db=db)
    
    await file_services.update_file_status(file_id=file_id,
                                     status=FileStatus.PARSED,
                                     db=db)

    """
    
    CHUNKED checkpoint

        chunking file
        save chunked file on disc
    
    """
    chunks = await file_chunk.chunk_document(parsed_document=parsed_object)
    chunks_file_path = await file_chunk.save_chunks_on_disc(chunks=chunks)
    await update_file_status(file_id=file_id, status=FileStatus.CHUNKED, db=db)
    await file_chunk.add_chunked_info_to_db(file_id=file_id, chunks=chunks, chunks_file_path=chunks_file_path, db=db)

    return file_db_info
    



@router.delete("/delete_file/{file_id}", status_code=status.HTTP_200_OK)
async def delete_file_endpoint(file_id: str, db: AsyncSession=Depends(get_db)):
    file = await file_services.find_file_by_id(file_id, db)
    
    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found file with id: {file_id}")

    await file_delete_logic.delete_file_from_disc(file)
    await file_delete_logic.delete_file_from_db(file, db)



    return {"message": f"File id: {file_id} has been deleted"}

@router.get("/find_file/{file_name}", status_code=status.HTTP_200_OK)
async def find_post_by_name_endpoint(file_name: str, db: AsyncSession=Depends(get_db)):
    file = await file_services.find_file_by_name(file_name, db)
    
    if file is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found file with id: {file_name}")
    
    return file

@router.get("/all_files", status_code=status.HTTP_200_OK)
async def get_all_files_endpoint(db: AsyncSession=Depends(get_db)) -> list[schemas_file.FileResponse]:
    return await file_services.get_all_files(db)

@router.get("/delete_file/delete_all_files")
async def delete_all_files_endpoint(db: AsyncSession=Depends(get_db)):
    files_list = await file_services.get_all_files(db)

    for file in files_list:
        await file_delete_logic.delete_file_from_disc(file)
        await file_delete_logic.delete_file_from_db(file, db)
    
    return {"message": "files delete"}