from pydantic import BaseModel


class PDFContent(BaseModel):
    uuid_pdf: str
    content: bytes