from sqlalchemy import String, DateTime, Boolean, ForeignKey, UUID as SQLUUID, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime, date
from nucleus.db.database import Base
from typing import List, Optional
from uuid import UUID, uuid4



class PersonalInformation(Base):
    __tablename__ = "personal_information"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True
    )

    # FK → Core Client table
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    client: Mapped["Client"] = relationship("Client", back_populates="personal_information")

    # marital status enum (Single, Married, Divorced, Widowed) → SINGLE, MARRIED, DIVORCED, WIDOWED
    marital_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Name refinement (non-core)
    middle_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Additional identity documents
    social_security_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    passport_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    power_of_attorney: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    #Yes/No/NA
    is_huf: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    huf_pan: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    huf_dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Karta (HUF manager) — the individual who signs & verifies the HUF return.
    # CBDT requires Verification.AssesseeVerPAN to be a person PAN (4th char "P"),
    # i.e. the karta's individual PAN, distinct from the HUF's own PAN.
    karta_pan: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    karta_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    
