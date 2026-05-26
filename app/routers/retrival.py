from fastapi import File, UploadFile, Depends, status, HTTPException, APIRouter, BackgroundTasks
from app.schemas import schemas_retrival

router = APIRouter(
    prefix="/question",
    tags=["Retrival"]
)

@router.post("/ask", status_code=status.HTTP_200_OK)
async def retrival(question: schemas_retrival.Question):

    #embeding pytania

    #wyszikowanie podobienstwa

    # zlozenie konteksu

    #odpowiedz llm