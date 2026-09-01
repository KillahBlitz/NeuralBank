from pydantic import BaseModel
from typing import List
from datetime import datetime


class GetFilesResponse(BaseModel):
    uuid: str
    upload_at: datetime
    file_name: str
    status: str
    file_size: int
    pages: int

class GetFilesListResponse(BaseModel):
    files_list: List[GetFilesResponse]