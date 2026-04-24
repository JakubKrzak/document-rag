import asyncio
import shutil


async def save_file_on_disc(file_object, file_content_hash):
    """
    
    Function saves file on disc and return file_path

    """
    name, ext = file_object.filename.rsplit(".", 1)
    file_path = f"disc/{name}_{file_content_hash[:8]}.{ext}"

    file_object.file.seek(0)
    with open(file_path, "wb") as b:
        await asyncio.to_thread(shutil.copyfileobj, file_object.file, b)
    
    return file_path