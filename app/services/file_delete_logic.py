from sqlalchemy.ext.asyncio import AsyncSession
from database import models
import os
import asyncio

async def delete_file_from_db(file_object: models.File, db: AsyncSession):
    await db.delete(file_object)
    await db.commit()


async def delete_file_from_disc(file_object: models.File):

    def _delete(file_object: models.File):
        if os.path.exists(file_object.file_path):
            os.remove(file_object.file_path)
    
        if os.path.exists(file_object.parsed_file_path):
            os.remove(file_object.parsed_file_path)

        if os.path.exists(file_object.chunks_path):
            os.remove(file_object.chunks_path)

            #chunks_disc/pdf_test_5692a551.jsonl
            #chunks_disc/pdf_test_5692a551.jsonl
    await asyncio.to_thread(_delete, file_object)


