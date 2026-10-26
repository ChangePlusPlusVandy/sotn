from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.db import DbSession
from app.routers import inquiries, programs

app = FastAPI(title="SOTN Intake API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inquiries.router)
app.include_router(inquiries.admin_router)

app.include_router(programs.router)
app.include_router(programs.admin_router)


@app.get("/health")
def health(db: DbSession):
    db.execute(text("select 1"))
    return {"ok": True}
