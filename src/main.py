import copy

from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseSettings

from . import configuration
from . import riot


class Settings(BaseSettings):
    app_name: str = "LoL genie"
    api_key: str = configuration.get_api_key()
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
app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

common_context = {
    "settings": settings,
    "messages": [],
}


def get_context():
    return copy.deepcopy(common_context)


@app.get("/")
def home(request: Request, context: dict = get_context()):
    context.update(
        {
            "request": request,
        }
    )
    return templates.TemplateResponse("home.html", context)


@app.get("/summoner/{region_code}/{summoner}")
def summoner_get(
    request: Request,
    summoner: str,
    region_code: str = "euw1",
    context: dict = get_context(),
):
    success_summoner_data, summoner_data = riot.get_summoner_data(
        region_code, summoner, settings.api_key
    )
    print(summoner_data)
    if not success_summoner_data:
        context["messages"].append(
            ("error", f"Failed to retrieve summoner data: {summoner_data}")
        )
        success_last_games = {}
        last_games = {}
    else:
        success_last_games, last_games = riot.get_last_games(
            region_code,
            summoner_data["accountId"],
            settings.api_key,
            start_index=0,
            end_index=20,
        )
        print(last_games)
    context.update(
        {
            "request": request,
            "summoner_data": summoner_data,
            "last_games": last_games,
            "success": {
                "summoner_data": success_summoner_data,
                "last_games": success_last_games,
            },
        }
    )
    return templates.TemplateResponse("summoner.html", context)


@app.post("/summoner")
def summoner_form(
    request: Request,
    context: dict = get_context(),
    summoner: str = Form(...),
    region_code: str = Form(...),
):
    return RedirectResponse(
        url=f"/summoner/{region_code}/{summoner}", status_code=status.HTTP_303_SEE_OTHER
    )
