from __future__ import annotations

import random
from typing import Callable, Dict, Protocol, Sequence

from attr import dataclass

from models.game import Game
from models.player import Player


class TeamAllocator(Protocol):
    def __call__(self, game: Game) -> None: ...


_ALLOCATE_TEAMS_REGISTRY: Dict[str, TeamAllocator] = {}


def register_team_allocator(name: str) -> Callable[[TeamAllocator], TeamAllocator]:
    def deco(fn: TeamAllocator) -> TeamAllocator:
        _ALLOCATE_TEAMS_REGISTRY[name] = fn
        return fn

    return deco


def _assign_in_order(players: list[Player], team_size: int) -> None:
    """Given players in desired order, assign team numbers in contiguous blocks."""
    for i, p in enumerate(players):
        p.team = (i // team_size) + 1


@register_team_allocator("fixed")
def alloc_fixed(game: Game) -> None:
    # Keep current order; assign in blocks of team_size
    _assign_in_order(game.players, 2)


@register_team_allocator("random")
def alloc_random(game: Game) -> None:
    random.shuffle(game.players)
    _assign_in_order(game.players, 2)


@register_team_allocator("balanced")
def alloc_balanced_by_score(game: Game) -> None:
    alloc_random(game)


@dataclass
class TeamCombinations:
    combinations: list[list[tuple[Player, Player]]] | None = None

    def generate_unique_team_layouts(
        self,
        players: Sequence[Player],
    ) -> None:
        n = len(players)
        assert n % 2 == 0, "Number of players must be even"

        # Round-robin pairing algorithm
        players = list(players)
        layouts = []

        for _ in range(n - 1):
            pairs = [(players[i], players[-i - 1]) for i in range(n // 2)]
            layouts.append(pairs)
            players = [players[0]] + players[-1:] + players[1:-1]

        self.combinations = layouts


tc = TeamCombinations()


@register_team_allocator("rolling")
def alloc_rolling(game: Game) -> None:
    if tc.combinations is None:
        players = game.players
        random.shuffle(players)
        game.players = players
        tc.generate_unique_team_layouts(game.players)

    assert tc.combinations is not None
    combination = tc.combinations.pop(0)

    if not tc.combinations:
        tc.combinations = None  # Reset for next time

    for team, (p1, p2) in enumerate(combination, start=1):
        p1.team = team
        p2.team = team
