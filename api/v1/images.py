from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas import URLSubmit

image_router = APIRouter(tags=["images"], prefix="/images")


@image_router.post("/match-colour")
async def match_colour(url: URLSubmit, db: Session = Depends(get_db)):
    return url
