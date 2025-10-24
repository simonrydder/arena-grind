from __future__ import annotations

from collections.abc import Iterator
from typing import Callable, Dict, Protocol, Sequence

from models.champion import Champion
from models.game import Game


class ChampionSelector(Protocol):
    def __call__(self, game: Game) -> Iterator[tuple[Sequence[Champion], str]]: ...


_CHAMPION_SELECTION_METHOD: Dict[str, ChampionSelector] = {}


def register_champion_selection(
    name: str,
) -> Callable[[ChampionSelector], ChampionSelector]:
    def deco(fn: ChampionSelector) -> ChampionSelector:
        _CHAMPION_SELECTION_METHOD[name] = fn
        return fn

    return deco


def get_tag(game: Game) -> set[str]:
    tags = dict[str, int]()
    for champ in game.champions:
        if not champ.available:
            continue

        for tag in champ.tags:
            tags[tag] = tags.get(tag, 0) + 1

    available_tags = {tag for tag, count in tags.items() if count >= 2}

    return available_tags


def tag_iterator(game: Game) -> Iterator[str]:
    while tags := get_tag(game):
        for tag in tags:
            yield tag


@register_champion_selection("tags")
def tag_selection(game: Game) -> Iterator[tuple[Sequence[Champion], str]]:
    """Select champions based on tags."""
    for tag in tag_iterator(game):
        champions = [champ for champ in game.champions if tag in champ.tags]

        yield champions, tag
