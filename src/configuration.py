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
    regions: dict = {
        "EUW1": {"code": "EUW1", "host": "euw1.api.riotgames.com"},
        "BR1": {"code": "BR1", "host": "br1.api.riotgames.com"},
        "EUN1": {"code": "EUN1", "host": "eun1.api.riotgames.com"},
        "JP1": {"code": "JP1", "host": "jp1.api.riotgames.com"},
        "KR": {"code": "KR", "host": "kr.api.riotgames.com"},
        "LA1": {"code": "LA1", "host": "la1.api.riotgames.com"},
        "LA2": {"code": "LA2", "host": "la2.api.riotgames.com"},
        "NA1": {"code": "NA1", "host": "na1.api.riotgames.com"},
        "OC1": {"code": "OC1", "host": "oc1.api.riotgames.com"},
        "TR1": {"code": "TR1", "host": "tr1.api.riotgames.com"},
        "RU": {"code": "RU", "host": "ru.api.riotgames.com"},
    }

    def get_api_host(self, region_code):
        if not region_code in self.regions:
            raise Exception("Region code not recognised")
        else:
            return self.regions[region_code]["host"]


settings = Settings()