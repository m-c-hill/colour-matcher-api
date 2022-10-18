from core import models
from core.database import SessionLocal, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

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
        """
        Check if colour table is populated. If not, execute query in core/data to
        insert selection of colours for pixel comparison.
        """
        db = SessionLocal()
        c = db.query(models.Colour).first()
        if not c:
            with open("core/data/colours.sql") as file:
                query = text(file.read())
                db.execute(query)
                db.commit()

    return app
