from handlers.query_handler import QueryHandler
from handlers.command_handler import CommandHandler

from models.pdf_file_upload import PDFFileUpload, PDFStatus
from models.pdf_content import PDFContent
from models.response.pdf_upload_response import PDFUploadResponse

import datetime
import hashlib
import fitz


class UploadHandler:
    def __init__(self) -> None:
        self._qh = QueryHandler()
        self._ch = CommandHandler()

    async def upload_pdf_file(self, file):
        raw = await file.read()
        upload_file = datetime.datetime.now()
        file_name = file.filename
        file_size = len(raw)
        signature = hashlib.sha256(raw).hexdigest()
        with fitz.open(stream=raw, filetype="pdf") as doc:
            pages = len(doc)
        pdf_file_upload = PDFFileUpload(
            upload_at=upload_file,
            file_name=file_name,
            signature=signature,
            status=PDFStatus.INCOMPLETE,
            file_size=file_size,
            pages=pages)        
        try:
            self._ch.insert_pdf_file_upload(pdf_file_upload)

            content = PDFContent(
                uuid_pdf=pdf_file_upload.uuid,
                content=raw,
                pages=pages)
            self._ch.instert_pdf_content(content)
            pdf_file_upload.status = PDFStatus.PENDING
            self._ch.update_pdf_file_upload(pdf_file_upload)
            response = PDFUploadResponse(
                file_uuid=pdf_file_upload.uuid,
                uploaded_at=upload_file,
                file_name=file_name,
                file_size=file_size)
            
        except Exception as e:
            response = PDFUploadResponse(
                file_uuid=pdf_file_upload.uuid,
                uploaded_at=upload_file,
                file_name=file_name,
                file_size=file_size,
                error=str(e))
            
        return response
            




        