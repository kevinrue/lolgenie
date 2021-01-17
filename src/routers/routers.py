import copy

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .. import configuration
from .. import riot


router = APIRouter(prefix="")

templates = Jinja2Templates(directory="src/templates")

settings = configuration.settings

common_context = {
    "settings": settings,
    "messages": [],
}


def get_context():
    return copy.deepcopy(common_context)


@router.get("/")
def home(request: Request, context: dict = get_context()):
    context.update(
        {
            "request": request,
        }
    )
    return templates.TemplateResponse("home.html", context)


@router.get("/summoner/{region_code}/{summoner}")
def summoner_get(
    request: Request,
    summoner: str,
    region_code: str = "EUW1",
    context: dict = get_context(),
):
    # Initialize context
    extra_context = {"request": request, "success": {}}
    api_host = settings.get_api_host(region_code)
    # Query summoner data
    success_summoner_data, summoner_data = riot.get_summoner_data(api_host, summoner)
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
            api_host,
            summoner_data["accountId"],
            start_index=0,
            end_index=20,
        )
        # Add success status to context
        extra_context["success"]["last_games"] = success_last_games
    # Add champion data in each game
    if success_summoner_data and not success_last_games:
        # Add banner if the match history query failed
        context["messages"].append(
            ("error", f"Failed to retrieve match history data: {last_games}")
        )
    elif success_summoner_data and success_last_games:
        # Fetch champion data
        champions = riot.get_champions(release=settings.latest_release)
        champ_ids_to_names = riot.get_champions_map(champions, key="key", value="id")
        # Add champion data to each game, if the match history was succesfully queried
        for game in last_games["matches"]:
            game["champion_name"] = champ_ids_to_names[str(game["champion"])]
            game_datetime = riot.get_datetime_from_timestamp(game["timestamp"])
            game["datetime_readable"] = game_datetime.strftime("%H:%M - %B %d, %Y")
        # Add match history data to context
        extra_context["last_games"] = last_games
    # Update context
    context.update(extra_context)
    return templates.TemplateResponse("summoner.html", context)


@router.post("/summoner")
def summoner_form(
    request: Request,
    context: dict = get_context(),
    summoner: str = Form(...),
    region_code: str = Form(...),
):
    return RedirectResponse(
        url=f"/summoner/{region_code}/{summoner}", status_code=status.HTTP_303_SEE_OTHER
    )
