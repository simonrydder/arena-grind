from models.game import Game
from models.player import Player


def update_team_score(game: Game, team: int, placement: int) -> None:
    for player in game.players:
        if player.team == team:
            player.score += placement


def get_scoreboard(game: Game) -> list[Player]:
    return sorted(game.players, key=lambda p: p.score)


def allocate_teams(game: Game) -> None:
    for i, player in enumerate(game.players):
        player.team = (i % 2) + 1
