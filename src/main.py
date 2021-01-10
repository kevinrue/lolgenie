from fastapi import FastAPI, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import riot

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def index(request: Request):
    api_key = riot.get_api_key()
    context = {"request": request, "api_key": api_key}
    return templates.TemplateResponse("index.html", context)


@app.get("/summoner/{summoner}")
def summoner_get(request: Request, summoner: str):
    context = {"request": request, "summoner": summoner}
    return templates.TemplateResponse("summoner.html", context)


@app.post("/summoner")
def summoner_form(request: Request, summoner: str = Form(...)):
    return RedirectResponse(
        url=f"/summoner/{summoner}", status_code=status.HTTP_303_SEE_OTHER
    )
