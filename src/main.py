import copy

from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from .configuration import settings
from . import riot


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
    # Initialize context
    extra_context = {"request": request, "success": {}}
    # Query summoner data
    success_summoner_data, summoner_data = riot.get_summoner_data(
        region_code, summoner, settings.api_key
    )
    # Add success status to context
    extra_context["success"]["summoner_data"] = success_summoner_data
    # Add summoner data to context
    extra_context["summoner_data"] = summoner_data
    if not success_summoner_data:
        # Add banner if summoner data query failed
        context["messages"].append(
            ("error", f"Failed to retrieve summoner data: {summoner_data}")
        )
    else:
        # Query match history if summoner account id was successfully queried
        success_last_games, last_games = riot.get_last_games(
            region_code,
            summoner_data["accountId"],
            settings.api_key,
            start_index=0,
            end_index=20,
        )
        # Add success status to context
        extra_context["success"]["last_games"] = success_last_games
    # Add champion name in each game
    if success_summoner_data and not success_last_games:
        # Add banner if the match history query failed
        context["messages"].append(
            ("error", f"Failed to retrieve match history data: {last_games}")
        )
    if success_summoner_data and success_last_games:
        # Fetch champion data
        champions = riot.get_champions(release="11.1.1")
        # Add champion name to each game, if the match history was succesfully queried
        for game in last_games["matches"]:
            game["champion_name"] = riot.get_champion_name_from_id(
                str(game["champion"]), champions
            )
        # Add match history data to context
        extra_context["last_games"] = last_games
    # Update context
    context.update(extra_context)
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
