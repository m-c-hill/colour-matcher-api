from typing import List, Union

from sqlalchemy.orm import Session

from core import models


def load_colours(db: Session) -> List[models.Colour]:
    return db.query(models.Colour).all()


def get_colour_by_id(db: Session, id: int) -> Union[models.Colour, None]:
    return db.query(models.Colour).filter_by(id=id).one_or_none()


def get_colour_by_name(db: Session, name: str) -> Union[models.Colour, None]:
    return db.query(models.Colour).filter_by(name=name).one_or_none()


def get_image_by_url(db: Session, url: str) -> Union[models.Image, None]:
    return db.query(models.Image).filter(models.Image.url == url).one_or_none()


def create_image_record(db: Session, url: str, colour_id: int) -> Union[models.Image, None]:
    db_image = models.Image(url=url, matched_colour_id=colour_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
