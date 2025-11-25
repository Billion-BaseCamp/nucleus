from nucleus.db.database import Base
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.types import DateTime
import uuid

class File(Base):
    __tablename__ = "files"

    id:Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name:Mapped[str] = mapped_column(String, nullable=False)
    file_path:Mapped[str] = mapped_column(String, nullable=False)
    uploaded_by:Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    uploaded_at:Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)



