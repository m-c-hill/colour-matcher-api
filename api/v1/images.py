from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core import schemas, services
from core.database import get_db
from core.crud import get_image_by_url, load_colours

image_router = APIRouter(tags=["images"], prefix="/images")


@image_router.post("/match-colour")
async def match_colour(body: schemas.URLSubmit, db: Session = Depends(get_db)):
    url = body.url

    if not services.is_url_image(url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="URL contains no valid image content.",
        )

    image_record = get_image_by_url(db, url)
    if image_record:
        match = ""  # TODO: update to take into account stored image
    else:
        colours = load_colours(db)
        match = services.match_image_with_colour(url, colours)
        # TODO: save url, add crud function

    return schemas.ColourMatchResponse(
        url=url,
        matched_colour=match["matched_colour"],
        # avg_deviation=match["avg_deviation"],
    )
