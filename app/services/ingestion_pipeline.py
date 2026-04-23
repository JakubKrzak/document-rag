from sqlalchemy.ext.asyncio import AsyncSession
from database.models import FileStatus

#upload functions
from app.services.upload import save_file_on_disc, add_file_to_database

#parsing functions
from app.services.parsing import parsed_file_content, save_parsed_file_on_disc, add_parsed_info_to_db

#chunking functions
from app.services.chunking import chunk_document, save_chunks_on_disc, add_chunked_info_to_db

#embedding functions
from app.services.embedding import build_point, save_points_on_disk, add_embed_info_to_db, check_vectors_dim

#shared functions
from app.services.shared import update_file_status

async def run_upload(file, file_content_hash, db:AsyncSession):
    file_path = await save_file_on_disc(file_object=file, file_content_hash=file_content_hash)
    file_db_info = await add_file_to_database(
        file_name=file.filename, file_content_hash=file_content_hash,
        file_size=file.size, file_content_type=file.content_type,
        file_path=file_path, status=FileStatus.UPLOADED, db=db)
    return file_db_info, file_path

async def run_parse(file_id, file_path, db:AsyncSession):
    parsed_object = await parsed_file_content(file_path=file_path)
    parsed_file_path = await save_parsed_file_on_disc(parsed_file=parsed_object)
    await add_parsed_info_to_db(file_id=file_id, parsed_file_path=parsed_file_path,
                                pages=len(parsed_object.pages), db=db)
    await update_file_status(file_id=file_id, status=FileStatus.PARSED, db=db)
    return parsed_object

async def run_chunk(file_id, parsed_object, db:AsyncSession):
    chunks = await chunk_document(parsed_document=parsed_object)
    chunks_file_path = await save_chunks_on_disc(chunks=chunks)
    await add_chunked_info_to_db(file_id=file_id, chunks=chunks,
                                 chunks_file_path=chunks_file_path, db=db)
    await update_file_status(file_id=file_id, status=FileStatus.CHUNKED, db=db)
    return [chunk.model_dump() for chunk in chunks]

async def run_embed(file_id, chunks, db:AsyncSession):
    points = await build_point(chunks=chunks)
    embed_path = await save_points_on_disk(points=points)
    vectors_dim = check_vectors_dim(points=points)
    await add_embed_info_to_db(file_id=file_id, embed_path=embed_path,
                               vectors_dim=vectors_dim, db=db)
    await update_file_status(file_id=file_id, status=FileStatus.EMBEDDED, db=db)
    