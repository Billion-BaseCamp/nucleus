from nucleus.db.database import Base
from sqlalchemy import String, DateTime, Integer, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from uuid import UUID, uuid4

class UploadBatches(Base):
    __tablename__ = "upload_batches"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id:Mapped[UUID]=mapped_column(SQLUUID(as_uuid=True), nullable=False, index=True)
    pan_number:Mapped[str]=mapped_column(String, nullable=False)
    total_files:Mapped[int]=mapped_column(Integer, nullable=False)
    uploaded_at:Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now())
    