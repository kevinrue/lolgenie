from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseSettings

from . import configuration


class Settings(BaseSettings):
    app_name: str = "LoL genie"
    api_key: str = configuration.get_api_key()


settings = Settings()
app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

common_context = {"settings": settings}


@app.get("/")
def index(request: Request):
    context = common_context
    context.update(
        {
            "request": request,
        }
    )
    return templates.TemplateResponse("index.html", context)


@app.get("/summoner/{summoner}")
def summoner_get(request: Request, summoner: str):
    context = common_context
    context.update(
        {
            "request": request,
            "summoner": summoner,
        }
    )
    return templates.TemplateResponse("summoner.html", context)


@app.post("/summoner")
def summoner_form(request: Request, summoner: str = Form(...)):
    return RedirectResponse(
        url=f"/summoner/{summoner}", status_code=status.HTTP_303_SEE_OTHER
    )
