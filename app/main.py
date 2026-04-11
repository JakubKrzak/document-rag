from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import files, db_health


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(db_health.router)
app.include_router(files.router)

@app.get("/", tags=['status'])
def server_status():
    return {"status": "ok"}






  
