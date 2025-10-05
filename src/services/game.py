from collections import defaultdict

from models.game import Game
from models.player import Player
from stategies.allocate_teams import _ALLOCATE_TEAMS_REGISTRY


def update_team_score(game: Game, team: int, placement: int) -> None:
    for player in game.players:
        if player.team == team:
            player.score += 9 - placement


def get_scoreboard(game: Game) -> list[Player]:
    return sorted(game.players, key=lambda p: p.score)


def get_teams(game: Game) -> dict[int, list[Player]]:
    teams = defaultdict(list)
    for player in game.players:
        if player.team not in teams:
            teams[player.team] = []
        teams[player.team].append(player)
    return teams


def allocate_teams(game: Game) -> None:
    """Dispatch to the chosen team allocation strategy."""
    key = getattr(game, "team_allocation_method", "fixed")
    try:
        fn = _ALLOCATE_TEAMS_REGISTRY[key]
    except KeyError:
        raise ValueError(
            f"Unknown team allocation method: {key!r}. Available: {sorted(_ALLOCATE_TEAMS_REGISTRY)}"
        )
    fn(game)
