
from models.repository.pdf_content_repository import PDFContentRepository
from models.repository.pdf_file_repository import PDFFileRepository


class QueryHandler:
    def __init__(self, 
                 pdf_file_repository: PDFFileRepository = None,
                 pdf_content_repository: PDFContentRepository = None):
        
        self._pdf_file_repository = pdf_file_repository or PDFFileRepository()
        self._pdf_content_repository = pdf_content_repository or PDFContentRepository()

    def get_pending_records(self):
        return self._pdf_file_repository.get_pending()

    def count_by_signature(self, signature) -> int:
        return self._pdf_file_repository.count_by_signature(signature)