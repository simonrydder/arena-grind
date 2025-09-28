# src/database/models/game.py
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class Game(Base):
    """
    Persists Game(name, players, round). Players are joined through GamePlayer.
    Dataclass reference: models/game.py. :contentReference[oaicite:6]{index=6}
    """

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    round: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    # Association collection
    game_players = relationship(
        "GamePlayer",
        back_populates="game",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Convenience: direct list of Player via association
    players = relationship(
        "Player",
        secondary="game_players",
        viewonly=True,
        lazy="selectin",
    )
