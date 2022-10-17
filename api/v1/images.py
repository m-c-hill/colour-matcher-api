from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core import services
from core import schemas
from core.database import get_db

image_router = APIRouter(tags=["images"], prefix="/images")


@image_router.post("/match-colour")
async def match_colour(body: schemas.URLSubmit, db: Session = Depends(get_db)):
    url = body.url

    if not services.validate_url(url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="URL contains no valid png image.",
        )

    match = services.match_colour(url)

    return schemas.ColourMatchResponse(
        url=url,
        closest_colour=match["closest_colour"],
        true_colour=match["true_colour"],
    )
