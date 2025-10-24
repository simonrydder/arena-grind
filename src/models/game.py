from dataclasses import dataclass, field
from datetime import datetime

from models.champion import Champion
from models.player import Player
from services.champion import create_champion
from services.lol import fetch_champion_data


@dataclass
class Game:
    name: str
    players: list[Player]
    round: int = 0
    champions: list[Champion] = field(
        default_factory=lambda: [create_champion(c) for c in fetch_champion_data()]
    )
    created_at: datetime = field(default_factory=datetime.now)
    team_allocation_method: str = "rolling"
    champion_selection_method: str = "tags"

    def __repr__(self) -> str:
        return (
            f"Game(name={self.name!r}, players={self.players!r}, "
            f"round={self.round}, created_at={self.created_at!r}, "
            f"team_allocation_method={self.team_allocation_method!r}, "
            f"champion_selection_method={self.champion_selection_method!r})"
        )
