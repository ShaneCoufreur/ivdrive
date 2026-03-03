import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, generate_uuid


class Announcement(Base):
    """A system-wide broadcast message created by admins."""

    __tablename__ = "announcements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    # type: info | success | warning | critical
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="info")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    user_announcements: Mapped[list["UserAnnouncement"]] = relationship(
        back_populates="announcement", cascade="all, delete-orphan", lazy="selectin"
    )

    @property
    def is_active(self) -> bool:
        if self.expires_at is None:
            return True
        return datetime.now(UTC) < self.expires_at


class UserAnnouncement(Base):
    """Tracks dismissal of an announcement per user."""

    __tablename__ = "user_announcements"

    __table_args__ = (
        UniqueConstraint("user_id", "announcement_id", name="uq_user_announcement"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=generate_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    announcement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("announcements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dismissed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    announcement: Mapped["Announcement"] = relationship(
        back_populates="user_announcements", lazy="selectin"
    )
