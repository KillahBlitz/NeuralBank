from datetime import datetime

from models.repository.pdf_content_repository import PDFContentRepository
from models.repository.pdf_file_repository import PDFFileRepository
from models.repository.image_file_repository import ImageFileRepository


class QueryHandler:
    def __init__(self, 
                 pdf_file_repository: PDFFileRepository = None,
                 pdf_content_repository: PDFContentRepository = None,
                 image_file_repository: ImageFileRepository = None):
        
        self._pdf_file_repository = pdf_file_repository or PDFFileRepository()
        self._pdf_content_repository = pdf_content_repository or PDFContentRepository()
        self._image_file_repository = image_file_repository or ImageFileRepository()

    def get_pending_records(self):
        return self._pdf_file_repository.get_pending()

    def count_by_signature(self, signature: str) -> int:
        return self._pdf_file_repository.count_by_signature(signature)

    def get_pdf_by_uuid(self, uuid):
        return self._pdf_content_repository.get_pdf_by_uuid(uuid)

    def get_files_list(self, start_date: datetime, end_date: datetime):
        return self._pdf_file_repository.get_files_list(start_date, end_date)

    def get_images_by_uuid_file(self, file_uuid: str):
        return self._image_file_repository.get_images_by_file_uuid(file_uuid)

    def get_image_by_uuid_and_page(self, file_uuid: str, page: int):
        return self._image_file_repository.get_image_by_file_uuid_and_page(file_uuid, page)

    def count_pages_by_file_uuid(self, file_uuid: str) -> int:
        return self._image_file_repository.count_pages_by_file_uuid(file_uuid)