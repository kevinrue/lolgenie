from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import routers

app = FastAPI()
app.include_router(routers.router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
