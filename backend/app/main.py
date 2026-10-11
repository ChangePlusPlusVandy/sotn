from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.db import DbSession
from app.routers import intakes

app = FastAPI(title="SOTN Intake API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(intakes.router)
app.include_router(intakes.admin_router)


@app.get("/health")
def health(db: DbSession):
    db.execute(text("select 1"))
    return {"ok": True}
