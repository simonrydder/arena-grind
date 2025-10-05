from models.game import Game


def save(game: Game) -> None:
    # TODO: implement saving logic
    print("Tried to save game:", game)

    pass


def load(name: str) -> Game:
    # TODO: implement loading logic
    return Game(name=name, players=[])
