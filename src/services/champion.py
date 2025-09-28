from models.champion import Champion
from models.lol import ChampionDragon
from services.lol import get_image_icon_url


def create_champion(champion_data: ChampionDragon) -> Champion:
    image = champion_data.image.full
    version = champion_data.version

    return Champion(
        name=champion_data.name,
        available=True,
        image_url=get_image_icon_url(image, version),
        tags=champion_data.tags,
    )
