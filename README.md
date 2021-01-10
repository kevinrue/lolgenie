
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

# FastAPI requirements

In order to run this app in development mode:
  1. Clone repository
  2. Create a python environment using the `requirment.txt` file
  3. Run the webserver using `uvicorn`: `uvicorn src.main:app --reload`

# Riot requirements

This repository is meant to host code for querying and processing data from the Riot Games API.

## Requirements

To develop and use this code, you will need:

- a Riot Games Developer account at <https://developer.riotgames.com/>
- a Riot Games API key

In your `.bashrc`, `.zshrc`, or equivalet, export the Riot Games API key as `RIOT_API_KEY`.

```
export RIOT_API_KEY="RGAPI-blah-blah-blah"
```
