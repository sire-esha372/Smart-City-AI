from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database.database import engine
from .database.models import Base

from .routers.traffic import router as traffic_router
from .routers.power import router as power_router
from .routers.pollution import router as pollution_router
from .routers.emergency import router as emergency_router
from .routers.waste import router as waste_router
from .routers.citizen import router as citizen_router
from .routers.rag import router as rag_router
from .routers.agents import router as agents_router
from .routers.dashboard import router as dashboard_router
from .routers.history import router as history_router

# ==========================================
# CREATE DATABASE
# ==========================================

Base.metadata.create_all(bind=engine)

# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

# ==========================================
# FASTAPI
# ==========================================

app = FastAPI(
    title="Smart City AI Platform",
    version="1.0.0"
)

# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Smart City AI Platform!"
    }

# ==========================================
# ROUTERS
# ==========================================

app.include_router(traffic_router)
#app.include_router(power_router)
#app.include_router(pollution_router)
#app.include_router(emergency_router)
#app.include_router(waste_router)
#app.include_router(citizen_router)
#app.include_router(rag_router)
#app.include_router(agents_router)
#app.include_router(dashboard_router)
#app.include_router(history_router)