from nucleus.db.database import Base
from sqlalchemy import UUID as SQLUUID, String, ForeignKey, DateTime, Boolean
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime


class RuleValidations(Base):
    __tablename__ = "rule_validations"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    rule_id: Mapped[str] = mapped_column(String, nullable=False)
    rule_description: Mapped[str] = mapped_column(String, nullable=False)

    quarter_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("quarters.id", ondelete="CASCADE"),
        nullable=False
    )

    advisor_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False)

    override_rule: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    comments: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="rule_validations")