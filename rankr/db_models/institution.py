from typing import List, TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from rankr.db_models.base import Base

if TYPE_CHECKING:
    from rankr.db_models.acronym import Acronym
    from rankr.db_models.alias import Alias
    from rankr.db_models.link import Link
    from rankr.db_models.ranking import Ranking
    from rankr.db_models.type import Type


class Institution(Base):
    __tablename__ = "institution"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    grid_id: str = Column(String(15), unique=True, nullable=False)
    name: str = Column(String(255), nullable=False)
    wikipedia_url: str = Column(String(255))
    established: int = Column(Integer)
    lat: str = Column(String(63))
    lng: str = Column(String(63))
    city: str = Column(String(63))
    state: str = Column(String(63))
    country: str = Column(String(63))
    country_code: str = Column(String(2))

    # Relationships
    acronyms: List["Acronym"] = relationship(
        "Acronym", back_populates="institution", cascade="all, delete-orphan"
    )
    aliases: List["Alias"] = relationship(
        "Alias", back_populates="institution", cascade="all, delete-orphan"
    )
    links: List["Link"] = relationship(
        "Link", back_populates="institution", cascade="all, delete-orphan"
    )
    rankings: List["Ranking"] = relationship(
        "Ranking", back_populates="institution", cascade="all, delete-orphan"
    )
    types: List["Type"] = relationship(
        "Type", back_populates="institution", cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if k in self.__table__.c}
        super().__init__(**kwargs)

    def __repr__(self):
        return f"{self.id} - {self.grid_id}: {self.name}"