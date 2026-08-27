from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.storage.database import Base


class EventRecord(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    event_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
    )

    format: Mapped[str] = mapped_column(
        String(32),
        index=True,
    )

    plugin: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )

    vendor: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )

    product: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    source_ip: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )

    destination_ip: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )

    action: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )

    raw_payload: Mapped[str] = mapped_column(
        Text,
    )

    normalized_json: Mapped[str] = mapped_column(
        Text,
    )

    sha256: Mapped[str] = mapped_column(
        String(64),
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )