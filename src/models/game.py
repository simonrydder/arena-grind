from dataclasses import dataclass

from models.player import Player


@dataclass
class Game:
    name: str
    players: list[Player]
    round: int = 0
