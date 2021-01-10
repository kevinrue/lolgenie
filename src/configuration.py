import os

def get_api_key():
    key = os.environ['RIOT_API_KEY']
    return key
