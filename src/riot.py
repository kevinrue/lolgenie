import requests

from .configuration import settings


def get_json(url):
    """
    Returns GET request OK status and content as JSON
    """
    res = requests.get(url)
    return res.ok, res.json()


def get_summoner_data(region, summoner_name, api_key):
    """
    Returns summoner data in JSON format and request OK status.

    Reference: https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName
    """
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    return get_json(url)


def get_last_games(region, encrypted_account_id, api_key, start_index=0, end_index=20):
    """
    Returns latest games data in JSON format and request OK status

    Reference: https://developer.riotgames.com/apis#match-v4/GET_getMatchlist
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{encrypted_account_id}?api_key={api_key}&beginIndex={start_index}&endIndex={end_index}"
    return get_json(url)


def get_champions(release=settings.latest_release):
    """
    Returns champions data.

    Reference: https://developer.riotgames.com/docs/lol#data-dragon_champions
    """
    url = f"http://ddragon.leagueoflegends.com/cdn/{release}/data/en_US/champion.json"
    success, query = get_json(url)
    if not success:
        pass  #  Do something
    champions = query["data"]
    return champions


def get_champion_name_from_id(id, champions):
    """
    Returns a list of champion names from their identifiers.

    Reference: https://gist.github.com/4dams/1808b051c4a3419e96f20ec4d19d2124

    Usage:
        champions = get_champions("11.1.1")
        get_champion_name_from_id("120", champions)
    """
    # TODO: A more optimised way to fetch the champion name could be a for loop that interrupts as soon as the id is matched.
    # TODO: 'IndexError: pop from empty list' if the id cannot be matched
    for champion in champions.values():
        if champion["key"] == id:
            return champion["id"]
    raise Exception("Champion not found")


def get_champion_names_from_ids(ids, release=settings.latest_release):
    """
    Returns a list of champion names from their identifiers.

    Reference: https://gist.github.com/4dams/1808b051c4a3419e96f20ec4d19d2124

    Usage:
        champions = get_champions(release)
        get_champion_names_from_ids(["1","120","120"])
    """
    names = [get_champion_name_from_id(id, champions) for id in ids]
    return names