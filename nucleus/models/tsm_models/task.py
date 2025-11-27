import uuid
from datetime import date, datetime
from uuid import UUID

from sqlalchemy import ARRAY, Boolean, DateTime, Enum, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleus.core.constants import IST_TIMEZONE
from nucleus.db.database import Base
from nucleus.core.constants import ACCEPTANCE_STATUS


class TaskAssignee(Base):
    __tablename__ = "task_assignees"

    task_id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.task_id", ondelete="CASCADE"), primary_key=True
    )
    advisor_id: Mapped[UUID] = mapped_column(
        ForeignKey("advisors.id", ondelete="CASCADE"), primary_key=True
    )


class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[UUID] = mapped_column(
        primary_key=True, index=True, default=uuid.uuid4
    )

    parent_task_id: Mapped[UUID] = mapped_column(
        ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=True, index=True
    )

    subtasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="parent",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    parent: Mapped["Task"] = relationship(
        "Task", back_populates="subtasks", remote_side="Task.task_id"
    )

    is_parent_task: Mapped[bool] = mapped_column(default=True)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("advisors.id"))

    title: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String, nullable=True)

    status: Mapped[str] = mapped_column(String)
    
    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
    )

    start_date: Mapped[datetime] = mapped_column(nullable=True)

    due_date: Mapped[datetime] = mapped_column(nullable=True)

    completed_date: Mapped[datetime] = mapped_column(nullable=True)

    acceptance_status: Mapped[ACCEPTANCE_STATUS] = mapped_column(
        Enum(ACCEPTANCE_STATUS, native_enum=False), nullable=True
    )

    rejection_reason: Mapped[str] = mapped_column(String, nullable=True)
    rejection_by: Mapped[UUID] = mapped_column(ForeignKey("advisors.id"), nullable=True)

    is_shared: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default=text("false")
    )

    completion_percentage: Mapped[int] = mapped_column(default=0)

    last_modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
        onupdate=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
        nullable=True,
    )
    modified_by: Mapped[UUID] = mapped_column(ForeignKey("advisors.id"), nullable=True)

    assignees: Mapped[list["Advisor"]] = relationship(
        "Advisor",
        secondary="task_assignees",
        back_populates="assigned_tasks",
        passive_deletes=True,
    )

    assigned_by: Mapped[UUID] = mapped_column(ForeignKey("advisors.id"), nullable=True)

    file_uploads: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id"), nullable=True)

    chat_messages: Mapped[list["TaskChatMessage"]] = relationship(
        "TaskChatMessage",
        back_populates="task",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
