

from fastapi import File, UploadFile, Depends, status, HTTPException, APIRouter
from app.services import file_delete_logic, upload_file_logic, file_services , file_parsed_content, file_chunk
from app.schemas import schemas_file
from database.database_engine import get_db
from config.settings import ALLOWED_TYPES, DOCLING_ALLOWED_TYPES
from sqlalchemy.orm import Session
from app.logger.log_conf import get_logger
logger = get_logger(__name__)

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

    if file.content_type not in DOCLING_ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"not allowed type")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing content")

    file_exists, file_content_hash = upload_file_logic.check_file_exists(content, db)

    if file_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"File |{file.filename}| exists")
    
    try:

        step = f"saving file on disc | file:{file.filename}"
        logger.info(f"start file processing | file_name: {file.filename}")        
        file_path = await upload_file_logic.save_file_on_disc(file_object=file, file_content_hash=file_content_hash)
        logger.info(f"file saved on disc | {file.filename}")

        step = f"parsing file | file:{file.filename}"
        parsed_object = await file_parsed_content.parsed_file_content(file_path=file_path)
        logger.info(f"parsed file | file_name: {file.filename} | pages: {len(parsed_object.pages)} | size: {file.size}")

        step = f"saving parsed file on disc | file:{file.filename}"
        parsed_file_path = await file_parsed_content.save_parsed_file_on_disc(parsed_file=parsed_object)
        logger.info(f"parsed file saved on disc | file_name:{file.filename}")

        step = f"chunking document | file_name:{file.filename}"
        chunks = await file_chunk.chunk_document(parsed_document=parsed_object)
        logger.info(f"chunking file | file_name:{file.filename} | chunks:  {len(chunks)}")

    
        step = f"adding file to database | file_name:{file.filename}"
        file_db_info = upload_file_logic.add_file_to_database(file_name=file.filename,
                                            file_content_hash=file_content_hash,
                                            file_size=file.size,
                                            file_content_type=file.content_type,
                                            parsed_file_path=parsed_file_path,
                                            file_path=file_path,
                                            pages= len(parsed_object.pages),
                                            db=db)
        logger.info(f"file added to database| file_id{file_db_info.id} | file_name:{file.filename}")


        return file_db_info
    
    except Exception as e:
        logger.exception(f"Error on step: {step} | file_name{file.filename} | {e}")


@router.delete("/delete_file/{file_id}", status_code=status.HTTP_200_OK)
def delete_file_enpoint(file_id: str, db: Session=Depends(get_db)):
    file = file_services.find_file_by_id(file_id, db)
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found file with id: {file_id}")

    file_delete_logic.delete_file_from_db(file, db)
    file_delete_logic.delete_file_from_disc(file)

    return {"message": f"File id: {file_id} has been deleted"}

@router.get("/find_file/{file_name}", status_code=status.HTTP_200_OK)
def find_post_by_name_enpoint(file_name: str, db: Session=Depends(get_db)):
    file = file_services.find_file_by_name(file_name, db)
    
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found file with id: {file_name}")
    
    return file

@router.get("/all_files", status_code=status.HTTP_200_OK)
def get_all_files_endpoint(db: Session=Depends(get_db)) -> list[schemas_file.FileResponse]:
    return file_services.get_all_files(db)