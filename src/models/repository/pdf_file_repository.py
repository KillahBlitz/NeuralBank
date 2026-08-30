from sqlalchemy import Column, String, Integer, DateTime, Enum as SAEnum, BigInteger


from services.db_conection import Base, SessionLocal
from models.pdf_file_upload import PDFFileUpload, PDFStatus

class PDFFileUploadRecord(Base):
    __tablename__ = "pdf_file"

    uuid = Column(String, primary_key=True)
    upload_at = Column(DateTime, nullable=False)
    file_name = Column(String, nullable=False)
    signature = Column(String, nullable=False)
    status = Column(SAEnum(PDFStatus), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    pages = Column(Integer, nullable=False)


class PDFFileRepository:
    def __init__(self):
        self.db = SessionLocal()

    def insert_pdf_file_upload(self, pdf_file: PDFFileUpload):
        record = PDFFileUploadRecord(
            uuid=pdf_file.uuid,
            upload_at=pdf_file.upload_at,
            file_name=pdf_file.file_name,
            signature=pdf_file.signature,
            status=pdf_file.status,
            file_size=pdf_file.file_size,
            pages=pdf_file.pages,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_pending(self) -> list[PDFFileUploadRecord]:
        return self.db.query(PDFFileUploadRecord).filter_by(status=PDFStatus.PENDING).all()

    def count_by_signature(self, signature: str) -> int:
        return self.db.query(PDFFileUploadRecord).filter_by(signature=signature).count()

    def update_pdf_file_upload(self, pdf_file_upload: PDFFileUpload):
        record = self.db.query(PDFFileUploadRecord).filter_by(uuid=pdf_file_upload.uuid).first()
        if record:
            record.status = pdf_file_upload.status
            self.db.commit()
            self.db.refresh(record)
        return record
