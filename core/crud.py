from typing import List, Tuple
from sqlalchemy.orm import Session
import models


def load_colours(db: Session) -> List[Tuple]:
    db.query(models.Colour).all()
