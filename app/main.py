from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text

from app.database import engine
from app.routers import drivers, vehicles

instrumentator = Instrumentator()


@asynccontextmanager
async def lifespan(app: FastAPI):
    instrumentator.expose(app)
    yield


app = FastAPI(title="FleetOps API", lifespan=lifespan)

instrumentator.instrument(app)

app.include_router(vehicles.router)
app.include_router(drivers.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ready", "db": "ok"}
    except Exception as e:
        return Response(status_code=503, content=str(e))
