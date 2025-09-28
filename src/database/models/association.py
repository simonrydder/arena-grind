# src/database/models/association.py
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class GamePlayer(Base):
    """
    Association table between Game and Player carrying per-game state.
    Mirrors your runtime model where score/team live on the player inside a given game
    (so we store those per game, not globally). See models in codebase.
    """

    __tablename__ = "game_players"
    __table_args__ = (
        UniqueConstraint("game_id", "player_id", name="uq_game_player_unique"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(
        ForeignKey("games.id", ondelete="CASCADE"), index=True
    )
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE"), index=True
    )

    # Per-game attributes (from your dataclasses/functions) :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}
    team: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    game = relationship("Game", back_populates="game_players")
    player = relationship("Player", back_populates="game_players")
