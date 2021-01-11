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


settings = Settings()
app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


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


@app.get("/summoner/{summoner}")
def summoner_get(request: Request, summoner: str, context: dict = get_context()):
    query = riot.get_summoner_data("euw1", summoner, settings.api_key)
    print(query)
    context.update(
        {
            "request": request,
            "query": query,
        }
    )
    return templates.TemplateResponse("summoner.html", context)


@app.post("/summoner")
def summoner_form(
    request: Request, context: dict = get_context(), summoner: str = Form(...)
):
    return RedirectResponse(
        url=f"/summoner/{summoner}", status_code=status.HTTP_303_SEE_OTHER
    )
