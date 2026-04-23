from sqlalchemy.ext.asyncio import AsyncSession                                                                            
from app.services.shared import find_file_by_id  

async def add_embed_info_to_db(file_id: str, embed_path: str, vectors_dim: int, db: AsyncSession):
    file = await find_file_by_id(file_id=file_id, db=db)
    file.embed_path = embed_path
    file.vectors_dim = vectors_dim
    await db.commit()
    await db.refresh(file)
    return True