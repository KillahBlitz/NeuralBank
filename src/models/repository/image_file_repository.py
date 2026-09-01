from sqlalchemy import Column, LargeBinary, String, Integer, DateTime

from services.db_conection import Base, SessionLocal
from models.image_file import ImageFile

class ImageFileRecord(Base):
    __tablename__ = "image_file"

    uuid = Column(String, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    file_name = Column(String, nullable=False)
    file_bytes = Column(LargeBinary, nullable=False)
    signature = Column(String, nullable=False)
    page_number = Column(Integer, nullable=False)
    uuid_pdf = Column(String, nullable=False)
    extraction = Column(String, nullable=True)

class ImageFileRepository:
    def __init__(self):
        self.db = SessionLocal()

    def insert_image_file(self, image_file: ImageFile):
        record = ImageFileRecord(
            uuid=image_file.uuid,
            created_at=image_file.created_at,
            file_name=image_file.file_name,
            file_bytes=image_file.file_bytes,
            signature=image_file.signature,
            page_number=image_file.page_number,
            uuid_pdf=image_file.uuid_pdf,
            extraction=image_file.extraction,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_image_file_by_uuid(self, uuid: str) -> ImageFileRecord:
        return self.db.query(ImageFileRecord).filter(ImageFileRecord.uuid == uuid).first()

    def update_image_file(self, uuid, text) -> None:
        record = self.db.query(ImageFileRecord).filter(ImageFileRecord.uuid == uuid).first()
        record.extraction = text
        self.db.commit()

    def get_images_by_file_uuid(self, file_uuid: str):
        data = []
        records = self.db.query(ImageFileRecord).filter(ImageFileRecord.uuid_pdf == file_uuid).order_by(ImageFileRecord.page_number).all()
        for r in records:
            data.append({
                "file_bytes": r.file_bytes,
                "page": r.page_number,
                "uuid_pdf": r.uuid_pdf,
                "extraction": r.extraction,
            })
        return data

    def get_image_by_file_uuid_and_page(self, file_uuid: str, page: int):
        r = self.db.query(ImageFileRecord).filter(
            ImageFileRecord.uuid_pdf == file_uuid,
            ImageFileRecord.page_number == page,
        ).first()
        if not r:
            return None
        return {
            "file_bytes": r.file_bytes,
            "page": r.page_number,
            "uuid_pdf": r.uuid_pdf,
            "extraction": r.extraction,
        }

    def count_pages_by_file_uuid(self, file_uuid: str) -> int:
        return self.db.query(ImageFileRecord).filter(ImageFileRecord.uuid_pdf == file_uuid).count()
    

