from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.database_engine import get_db


router = APIRouter(
    prefix="/database",
    tags=['database_health']
)

@router.get("/health")
def db_connection(db: Session=Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}