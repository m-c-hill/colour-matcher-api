from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from core import models
from core.database import SessionLocal, engine

from .v1 import v1_router

SEED = False  # TODO: temporary solution to adding colours to database on start-up


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
        if SEED:
            db = SessionLocal()
            with open("core/data/colours.sql") as file:
                query = text(file.read())
                db.execute(query)
                db.commit()

    return app
