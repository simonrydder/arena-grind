from dataclasses import dataclass, field
from datetime import datetime

from models.player import Player


@dataclass
class Game:
    name: str
    players: list[Player]
    round: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    team_allocation_method: str = "fixed"
