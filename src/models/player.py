from dataclasses import dataclass


@dataclass
class Player:
    name: str
    score: int
    team: int
