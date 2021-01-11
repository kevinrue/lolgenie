
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# FastAPI requirements

In order to run this app in development mode, set up your workspace as follows:

  1. Clone repository
  2. Create a Conda environment using Conda: `conda create -n lolgenie python=3.8`
  3. Activate the Conda environment: `conda activate lolgenie`
  3. Restore the python environment using the `requirements.txt` file: `pip install -r requirements.txt`
  4. Run the webserver using `uvicorn`: `uvicorn src.main:app --reload`

Every time you come back to the project, prepare your workspace as follows:

1. Activate the Conda environment: `conda activate lolgenie`
2. Run the webserver using `uvicorn`: `uvicorn src.main:app --reload`

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
