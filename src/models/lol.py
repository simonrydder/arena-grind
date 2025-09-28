from enum import StrEnum

from pydantic import BaseModel


class Language(StrEnum):
    US = "en_US"
    FR = "fr_FR"


class InfoDragon(BaseModel):
    attack: int
    defense: int
    magic: int
    difficulty: int


class ImageDragon(BaseModel):
    full: str
    sprite: str
    group: str
    x: int
    y: int
    w: int
    h: int


class StatsDragon(BaseModel):
    hp: float
    hpperlevel: float
    mp: float
    mpperlevel: float
    movespeed: float
    armor: float
    armorperlevel: float
    spellblock: float
    spellblockperlevel: float
    attackrange: float
    hpregen: float
    hpregenperlevel: float
    mpregen: float
    mpregenperlevel: float
    crit: float
    critperlevel: float
    attackdamage: float
    attackdamageperlevel: float
    attackspeedperlevel: float
    attackspeed: float


class ChampionDragon(BaseModel):
    version: str
    id: str
    key: int
    name: str
    title: str
    blurb: str
    info: InfoDragon
    image: ImageDragon
    tags: list[str]
    partype: str
    stats: StatsDragon


class LolDataDragon(BaseModel):
    type: str
    format: str
    version: str
    data: dict[str, ChampionDragon]
