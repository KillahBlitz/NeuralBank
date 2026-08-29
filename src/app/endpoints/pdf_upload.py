from typing import Annotated
from fastapi import APIRouter, File, UploadFile

from handlers.upload_handler import UploadHandler

router = APIRouter()

@router.post("/")
async def upload_file(file: Annotated[UploadFile, File()]):
    uph = UploadHandler()
    response = await uph.upload_pdf_file(file)
    return response
