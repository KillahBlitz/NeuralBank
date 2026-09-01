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

@router.get("/{file_uuid}/page/{page}")
async def get_image_page(file_uuid: str, page: int):
    qdh = QueryDataHandler()
    response = await qdh.get_image_page(file_uuid, page)
    return response