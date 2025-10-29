from sqlalchemy import String, DateTime, UUID as SQLUUID, Boolean
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base

class DocumentsUpload(Base):
    __tablename__ = "documents_upload"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    subCategory: Mapped[str] = mapped_column(String, nullable=False)
    link_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    file_key: Mapped[str] = mapped_column(String, nullable=False)
    bucket_name: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    is_password_protected: Mapped[bool] = mapped_column(Boolean, default=False)
    password: Mapped[str] = mapped_column(String, nullable=True)
