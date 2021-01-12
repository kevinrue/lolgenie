import os

from pydantic import BaseSettings


def get_api_key():
    key = os.environ["RIOT_API_KEY"]
    return key


def get_latest_release():
    latest_release = os.environ.get("LATEST_RELEASE", "11.1.1")
    return latest_release


class Settings(BaseSettings):
    app_name: str = "LoL genie"
    api_key: str = get_api_key()
    latest_release = get_latest_release()
    # Regions (actually called platform) taken from https://developer.riotgames.com/docs/lol
    regions: list = [
        {"code": "EUW1", "host": "euw1.api.riotgames.com"},
        {"code": "BR1", "host": "br1.api.riotgames.com"},
        {"code": "EUN1", "host": "eun1.api.riotgames.com"},
        {"code": "JP1", "host": "jp1.api.riotgames.com"},
        {"code": "KR", "host": "kr.api.riotgames.com"},
        {"code": "LA1", "host": "la1.api.riotgames.com"},
        {"code": "LA2", "host": "la2.api.riotgames.com"},
        {"code": "NA1", "host": "na1.api.riotgames.com"},
        {"code": "OC1", "host": "oc1.api.riotgames.com"},
        {"code": "TR1", "host": "tr1.api.riotgames.com"},
        {"code": "RU", "host": "ru.api.riotgames.com"},
    ]


settings = Settings()