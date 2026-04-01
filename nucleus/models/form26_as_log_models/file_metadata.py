from nucleus.db.database import Base
from sqlalchemy import String, DateTime, Integer, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey

class FileMetadata(Base):
    __tablename__ = "file_metadata"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    batch_id:Mapped[UUID]=mapped_column(SQLUUID(as_uuid=True), ForeignKey("upload_batches.id", ondelete="CASCADE"), nullable=False, index=True)
    file_name:Mapped[str]=mapped_column(String, nullable=False)
    s3_key:Mapped[str]=mapped_column(String, nullable=False)
    assessment_year:Mapped[str]=mapped_column(String, nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())