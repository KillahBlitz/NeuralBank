from models.repository.pdf_file_repository import PDFFileRepository
from models.repository.pdf_content_repository import PDFContentRepository

from models.pdf_file_upload import PDFFileUpload
from models.pdf_content import PDFContent

class CommandHandler:
    def __init__(self, 
                 pdf_file_repository: PDFFileRepository = None,
                 pdf_content_repository: PDFContentRepository = None):
        
        self._pdf_file_repository = pdf_file_repository or PDFFileRepository()
        self._pdf_content_repository = pdf_content_repository or PDFContentRepository()

    def insert_pdf_file_upload(self, pdf_file: PDFFileUpload):
        return self._pdf_file_repository.insert_pdf_file_upload(pdf_file)
    
    def update_pdf_file_upload(self, pdf_file_upload: PDFFileUpload):
        return self._pdf_file_repository.update_pdf_file_upload(pdf_file_upload)
    
    def instert_pdf_content(self, pdf_content: PDFContent):
        return self._pdf_content_repository.insert_pdf_content(pdf_content)
