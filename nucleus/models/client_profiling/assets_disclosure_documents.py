from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    UniqueConstraint,
    ForeignKey,
    UUID as SQLUUID,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class AssetsDisclosureDocuments(Base):
    __tablename__ = "assets_disclosure_documents"
    
    __table_args__ = (
        UniqueConstraint("sha256_hash", "financial_year_id", name="uq_assets_doc_client_hash"),
    )
    

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    financial_year_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id"),
        nullable=True,
        index=True,
    )
    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")

    client_email: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    content_type: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    
    

    file_size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=True,
    )

    sha256_hash: Mapped[str] = mapped_column(
        String(64),  # SHA256 hash is always 64 hex characters
        nullable=False,
    )
    
    s3_key: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


