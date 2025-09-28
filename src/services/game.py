from collections import defaultdict

from models.game import Game
from models.player import Player


def update_team_score(game: Game, team: int, placement: int) -> None:
    for player in game.players:
        if player.team == team:
            player.score += placement


def get_scoreboard(game: Game) -> list[Player]:
    return sorted(game.players, key=lambda p: p.score)


def get_teams(game: Game) -> dict[int, list[Player]]:
    teams = defaultdict(list)
    for player in game.players:
        if player.team not in teams:
            teams[player.team] = []
        teams[player.team].append(player)
    return teams
