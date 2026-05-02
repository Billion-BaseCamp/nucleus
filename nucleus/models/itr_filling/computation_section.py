"""Shared enum for computation workflow status on ITR schedule roots."""

from __future__ import annotations

import enum


class ComputationSectionStatus(str, enum.Enum):
    """Per-head workflow: not touched → being edited → user-marked complete."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
