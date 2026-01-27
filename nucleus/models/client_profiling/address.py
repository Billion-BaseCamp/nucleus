from nucleus.db.database import Base
from sqlalchemy import String, ForeignKey, UUID as SQLUUID, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import text
from enum import Enum as PyEnum


class AddressType(PyEnum):
    PRIMARY = "Primary"
    SECONDARY = "Secondary"



class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    client: Mapped["Client"] = relationship("Client", back_populates="addresses")

    address_type: Mapped[AddressType] = mapped_column(Enum(AddressType), nullable=False, 
                default=AddressType.PRIMARY, server_default=text(" 'Primary' "))

    address_line1: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pincode: Mapped[Optional[str]] = mapped_column(String, nullable=True)