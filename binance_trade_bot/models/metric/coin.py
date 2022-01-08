from datetime import datetime as _datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from .base import Base
from .run import Run


class Coin(Base):
    __tablename__ = "coin"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.id"))
    ticker = Column(String)

    def __init__(
        self,
        ticker: str,
    ):
        self.ticker= ticker

    def info(self):
        return {
            "run_id": self.run_id,
            "ticker": self.ticker
        }
