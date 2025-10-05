from __future__ import annotations

import random
from typing import Callable, Dict, Protocol

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
