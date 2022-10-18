from typing import List, Tuple

from sqlalchemy.orm import Session

from core import models


def load_colours(db: Session) -> List[models.Colour]:
    return db.query(models.Colour).all()


def get_image_by_url(db: Session, url: str):
    return db.query(models.Image).filter(models.Image.url == url).one_or_none()
