# src/database/models/player.py
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class Player(Base):
    """
    Base player identity. Score/team are per-game in GamePlayer to match runtime logic,
    while the pure Player holds identity info (name). Dataclass reference: models/player.py. :contentReference[oaicite:7]{index=7}
    """

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)

    # Backref to association rows
    game_players = relationship(
        "GamePlayer",
        back_populates="player",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
