import requests

from . import configuration, other_utils

settings = configuration.settings

################################################
######## Helper functions
################################################
def get_json(url, api_key=settings.api_key):
    """
    Returns GET request OK status and content as JSON
    """
    headers = {"X-Riot-Token": api_key}
    res = requests.get(url, headers=headers)
    return res.ok, res.json()


def get_image_url(key, value, release=settings.latest_release):
    """
    Returns the URL of an image for multiple objects
    Params:
        - key: type of object
        - value: object identifier to build the url
        - release: Current release of the game
    """
    if key == "champion_name":
        return (
            f"http://ddragon.leagueoflegends.com/cdn/{release}/img/champion/{value}.png"
        )
    else:
        return None


################################################
######## Basic calls to Riot API
################################################
def get_summoner_data(api_host, summoner_name):
    """
    Returns summoner data in JSON format and request OK status.

    Reference: https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName
    """
    url = f"https://{api_host}/lol/summoner/v4/summoners/by-name/{summoner_name}"
    return get_json(url)


def get_summoner_league_data(api_host, encrypted_summoner_id):
    """
    Returns summoner league data in JSON format and request OK status.

    Reference: https://developer.riotgames.com/apis#league-v4/GET_getLeagueEntriesForSummoner
    """
    url = (
        f"https://{api_host}/lol/league/v4/entries/by-summoner/{encrypted_summoner_id}"
    )
    return get_json(url)


def get_last_matches(api_host, encrypted_account_id, start_index=0, end_index=20):
    """
    Returns latest matches data in JSON format and request OK status

    Reference: https://developer.riotgames.com/apis#match-v4/GET_getMatchlist
    """
    url = f"https://{api_host}/lol/match/v4/matchlists/by-account/{encrypted_account_id}?beginIndex={start_index}&endIndex={end_index}"
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


def get_champions_map(champions, key="key", value="id"):
    """
    Returns a champion dict mapping key to value
    """
    return {champ[key]: champ[value] for champ in champions.values()}


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


def get_champion_names_from_ids(ids, champions, release=settings.latest_release):
    """
    Returns a list of champion names from their identifiers.

    Reference: https://gist.github.com/4dams/1808b051c4a3419e96f20ec4d19d2124

    Usage:
        champions = get_champions(release)
        get_champion_names_from_ids(["1","120","120"])
    """
    champ_ids_to_names = get_champions_map(champions, key="key", value="id")
    names = [champ_ids_to_names[id] for id in ids]
    return names


################################################
######## Enriched calls to Riot API
################################################
def get_last_matches_enriched(
    api_host,
    encrypted_account_id,
    start_index=0,
    end_index=20,
    release=settings.latest_release,
):
    """
    Returns latest matches data in JSON format enriched with:
    - Champion names
    - Datetime
    """
    # 1. Query match history
    success_last_matches, last_matches = get_last_matches(
        api_host,
        encrypted_account_id,
        start_index=0,
        end_index=20,
    )
    if not success_last_matches:
        raise Exception(f"Failed to retrieve match history data: {last_matches}")

    # 2. Add champion data in each match
    # Fetch champion data
    champions = get_champions(release=settings.latest_release)
    champ_ids_to_names = get_champions_map(champions, key="key", value="id")
    # Add champion data to each match, if the match history was succesfully queried
    for match in last_matches["matches"]:
        match["champion_name"] = champ_ids_to_names[str(match["champion"])]
        match_datetime = other_utils.get_datetime_from_timestamp(match["timestamp"])
        match["datetime_readable"] = match_datetime.strftime("%H:%M - %B %d, %Y")

    # TODO: 3. Add won/lost status to each match

    return success_last_matches, last_matches
