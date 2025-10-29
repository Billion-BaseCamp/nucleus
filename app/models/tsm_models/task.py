import uuid
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import IST_TIMEZONE
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )

    parent_task_id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.task_id"), nullable=True, index=True
    )

    subtasks: Mapped[list["Task"]] = relationship(
        "Task", back_populates="parent", cascade="all, delete-orphan"
    )

    parent: Mapped["Task"] = relationship(
        "Task", back_populates="subtasks", remote_side="Task.task_id"
    )

    is_parent_task: Mapped[bool] = mapped_column(default=True)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("advisors.id"))

    title: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String, nullable=True)

    service_category: Mapped[str] = mapped_column(String, nullable=True)

    difficulty_level: Mapped[str] = mapped_column(String)

    status: Mapped[str] = mapped_column(String)
    
    priority: Mapped[str] = mapped_column(String)

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
    )

    start_date: Mapped[datetime] = mapped_column(nullable=True)

    due_date: Mapped[date] = mapped_column(nullable=True)

    completed_date: Mapped[datetime] = mapped_column(nullable=True)

    share_cc: Mapped[str] = mapped_column(String, nullable=True)

    completion_percentage: Mapped[int] = mapped_column(default=0)

    last_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
        onupdate=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
        nullable=True,
    )
    modified_by: Mapped[UUID] = mapped_column(ForeignKey("advisors.id"), nullable=True)

    assigned_to: Mapped[UUID] = mapped_column(ForeignKey("advisors.id"), nullable=True)

    assigned_by:Mapped[UUID]=mapped_column(ForeignKey("advisors.id"), nullable =True)