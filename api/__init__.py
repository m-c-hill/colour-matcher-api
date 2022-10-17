from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import models
from core.database import SessionLocal, engine

from .v1 import v1_router


def create_app():
    models.Base.metadata.create_all(bind=engine)
    app = FastAPI(title="colour-matcher")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_router)

    @app.on_event("startup")
    def startup_populate_db():
        db = SessionLocal()
        # TODO: populate database with initial seed data?

    return app
