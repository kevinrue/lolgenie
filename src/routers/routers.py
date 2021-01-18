import copy

from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .. import configuration, riot, data_lib, other_utils


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
        success_last_matches, last_matches = riot.get_last_matches(
            api_host,
            summoner_data["accountId"],
            start_index=0,
            end_index=20,
        )
        # Add success status to context
        extra_context["success"]["last_matches"] = success_last_matches
        # Query league data if summoner account id was successfully queried
        (
            success_summoner_league_data,
            summoner_league_data,
        ) = riot.get_summoner_league_data(
            api_host,
            summoner_data["id"],
        )
        for league_data in summoner_league_data:
            league_data["wins_percent"] = round(
                league_data["wins"]
                / (league_data["wins"] + league_data["losses"])
                * 100,
                2,
            )
        # Add success status to context
        extra_context["success"]["summoner_league_data"] = success_summoner_league_data
        # Add summoner league data to context
        extra_context["summoner_league_data"] = summoner_league_data
    # Add champion data in each match
    if success_summoner_data and not success_last_matches:
        # Add banner if the match history query failed
        context["messages"].append(
            ("error", f"Failed to retrieve match history data: {last_matches}")
        )
    elif success_summoner_data and success_last_matches:
        # Fetch champion data
        champions = riot.get_champions(release=settings.latest_release)
        champ_ids_to_names = riot.get_champions_map(champions, key="key", value="id")
        # Add champion data to each match, if the match history was succesfully queried
        for match in last_matches["matches"]:
            match["champion_name"] = champ_ids_to_names[str(match["champion"])]
            match_datetime = other_utils.get_datetime_from_timestamp(match["timestamp"])
            match["datetime_readable"] = match_datetime.strftime("%H:%M - %B %d, %Y")
        # Add match history data to context
        extra_context["last_matches"] = last_matches
        # Add most played champions plot data
        extra_context["plot"] = {
            "most_played_champs": data_lib.most_played_champs_plot_data(last_matches)
        }
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
