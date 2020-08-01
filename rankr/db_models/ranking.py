import enum

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import DECIMAL, Enum, Integer, String

from config import DBConfig
from rankr.db_models.base import Base


RankingSystemEnum = enum.Enum(
    "RankingSystemEnum",
    {r_s: r_s for r_s in DBConfig.METRICS["ranking_systems"]},
)
MetricEnum = enum.Enum(
    "MetricEnum",
    {m["name"]: m["name"] for m in DBConfig.METRICS["metrics"].values()},
)
ValueTypeEnum = enum.Enum(
    "ValueTypeEnum",
    {m["type"]: m["type"] for m in DBConfig.METRICS["metrics"].values()},
)


class Ranking(Base):
    __tablename__ = "ranking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    institution_id = Column(Integer, ForeignKey("institution.id"))
    ranking_system = Column(Enum(RankingSystemEnum), nullable=False, index=True)
    year = Column(Integer)
    field = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    metric = Column(Enum(MetricEnum), nullable=False, index=True)
    value = Column(DECIMAL(13, 3), nullable=False)
    value_type = Column(Enum(ValueTypeEnum), nullable=False)

    # Relationships
    institution = relationship("Institution", back_populates="rankings")

    def __init__(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if k in self.__table__.c}
        super().__init__(**kwargs)
