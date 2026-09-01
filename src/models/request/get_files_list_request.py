from pydantic import BaseModel
from datetime import datetime

class GetFilesListRequest(BaseModel):
    start_date: datetime
    end_date: datetime