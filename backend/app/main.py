from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database.database import engine
from .database.models import Base

from .routers.traffic import router as traffic_router

Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Smart City AI Platform",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

@app.get("/")
def home():
    return {"message": "Welcome"}

app.include_router(traffic_router)