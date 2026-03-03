import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


AnnouncementType = Literal["info", "success", "warning", "critical"]


# ── Admin schemas ──────────────────────────────────────────────────────────────


class AnnouncementCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1)
    type: AnnouncementType = "info"
    expires_at: datetime | None = None


class AnnouncementResponse(BaseModel):
    id: uuid.UUID
    title: str
    message: str
    type: str
    created_at: datetime
    expires_at: datetime | None
    is_active: bool

    model_config = {"from_attributes": True}


# ── User schemas ───────────────────────────────────────────────────────────────


class UserAnnouncementResponse(BaseModel):
    """An announcement from the user's perspective, with dismissal info."""

    id: uuid.UUID
    title: str
    message: str
    type: str
    created_at: datetime
    expires_at: datetime | None
    dismissed: bool

    model_config = {"from_attributes": True}
