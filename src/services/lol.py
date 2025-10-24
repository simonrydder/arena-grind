from enum import StrEnum

import requests

from models.lol import ChampionDragon, LolDataDragon

BASE_URL = "https://ddragon.leagueoflegends.com/"


class Language(StrEnum):
    US = "en_US"
    FR = "fr_FR"


def fetch_versions() -> list[str]:
    url = f"{BASE_URL}api/versions.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_latest_version(versions: list[str]) -> str:
    return versions[0]


def get_data_url(version: str, language: str) -> str:
    url = f"{BASE_URL}cdn/{version}/data/{language}/champion.json"
    return url


def get_raw_champion_data(url: str) -> LolDataDragon:
    response = requests.get(url)
    response.raise_for_status()
    res = response.json()
    dd = LolDataDragon(**res)
    return dd


def fetch_champion_data() -> list[ChampionDragon]:
    versions = fetch_versions()
    latest = get_latest_version(versions)
    url = get_data_url(latest, Language.US)
    data_dragon = get_raw_champion_data(url)
    return get_champion_data(data_dragon)


def get_champion_data(data_dragon: LolDataDragon) -> list[ChampionDragon]:
    return list(data_dragon.data.values())


def get_image_icon_url(image: str, version: str) -> str:
    return f"{BASE_URL}cdn/{version}/img/champion/{image}"


def get_loading_image_url(id: str) -> str:
    return f"{BASE_URL}cdn/img/champion/loading/{id}_0.jpg"
