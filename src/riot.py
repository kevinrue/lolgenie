import requests


def get_json(url):
    """Returns GET request OK status and content as JSON"""
    res = requests.get(url)
    return res.ok, res.json()


def get_summoner_data(region, summoner_name, api_key):
    """
    Returns summoner data in JSON format and request OK status
    
    Reference: https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName
    """
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}"
    return get_json(url)

def get_last_games(region, encrypted_account_id, api_key, start_index = 0, end_index = 20):
    '''
    Returns latest games data in JSON format and request OK status

    Reference: https://developer.riotgames.com/apis#match-v4/GET_getMatchlist
    '''
    url = f"https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{encrypted_account_id}?api_key={api_key}&beginIndex={start_index}&endIndex={end_index}"
    return get_json(url)
