from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Colour(Base):
    __tablename__ = "colour"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    r = Column(Integer)
    g = Column(Integer)
    b = Column(Integer)
    images = relationship("Image")


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True)
    matched_colour_id = Column(Integer, ForeignKey("colour.id"))
