from typing import Annotated
from fastapi import APIRouter
from handlers.query_data_handler import QueryDataHandler
from models.request.get_files_list_request import GetFilesListRequest

router = APIRouter()

@router.post("/")
async def upload_file(filters: Annotated[GetFilesListRequest, "Filters for the query"]):
    qdh = QueryDataHandler()
    response = await qdh.get_files_list(filters)
    return response

@router.get("/{file_uuid}")
async def get_images_from_file(file_uuid: str):
    qdh = QueryDataHandler()
    response = await qdh.get_images_from_file(file_uuid)
    return response