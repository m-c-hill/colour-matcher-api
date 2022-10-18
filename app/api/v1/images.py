from core import crud, schemas, services
from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

image_router = APIRouter(tags=["images"], prefix="/images")


@image_router.post("/match-colour")
async def match_colour(body: schemas.URLSubmit, db: Session = Depends(get_db)):
    url = body.url

    if not services.is_url_image(url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="URL contains no valid image content.",
        )

    image_record = crud.get_image_by_url(db, url)
    if not image_record:
        colours = crud.load_colours(db)
        match = services.match_image_with_colour(url, colours)
        colour_id = crud.get_colour_by_name(db, match["matched_colour"]).id
        image_record = crud.create_image_record(db, url, colour_id)

    colour_name = crud.get_colour_by_id(db, image_record.matched_colour_id).name

    return schemas.ColourMatchResponse(
        url=url,
        matched_colour=colour_name,
    )
