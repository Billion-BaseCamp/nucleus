from sqlalchemy import UUID as SQLUUID
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from nucleus.db.database import Base
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.core.constants import CommentsCategory
from sqlalchemy import Enum



class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    comment: Mapped[str] = mapped_column(String, nullable=False)
    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[CommentsCategory] = mapped_column(Enum(CommentsCategory), nullable=False)
    created_by: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)