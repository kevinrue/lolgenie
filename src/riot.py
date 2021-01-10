import requests

def get_json(url):
    return requests.get(url).json()

def get_summoner_data(region, summoner_name, api_key):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    return get_json(url)
