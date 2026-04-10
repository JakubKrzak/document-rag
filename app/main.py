from fastapi import FastAPI, File, UploadFile
from typing import Annotated
import asyncio, shutil

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/file/upload")
async def upload_file(file: UploadFile=File(...)):
    
    with open(f"disc/{file.filename}", "wb") as buffer:
        await asyncio.to_thread(shutil.copyfileobj, file.file, buffer)

    return {"file_name": file.filename}
