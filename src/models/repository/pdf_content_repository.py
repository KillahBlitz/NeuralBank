from sqlalchemy import Column, String, Integer, BigInteger, LargeBinary, ForeignKey

from services.db_conection import Base, SessionLocal
from models.pdf_content import PDFContent


class PDFContentRecord(Base):
    __tablename__ = "pdf_content"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid_pdf = Column(String(40), ForeignKey("pdf_file.uuid", ondelete="CASCADE"), nullable=False, unique=True)
    content = Column(LargeBinary, nullable=False)
    pages = Column(Integer, nullable=False)


class PDFContentRepository:
    def __init__(self):
        self.db = SessionLocal()

    def insert_pdf_content(self, pdf_content: PDFContent):
        record = PDFContentRecord(
            uuid_pdf=pdf_content.uuid_pdf,
            content=pdf_content.content,
            pages=pdf_content.pages,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_pdf_by_uuid(self, uuid: str) -> PDFContentRecord | None:
        return self.db.query(PDFContentRecord).filter_by(uuid_pdf=uuid).first()
