import requests


def get_json(url):
    """Returns GET request OK status and content as JSON"""
    res = requests.get(url)
    return res.ok, res.json()


def get_summoner_data(region, summoner_name, api_key):
    """Returns summoner data in JSON format and request OK status"""
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    return get_json(url)
