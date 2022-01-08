from datetime import datetime as _datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from .base import Base


class Balance(Base):
    __tablename__ = "balance"

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey("sample.id"))
    ticker = Column(String)
    value = Column(Numeric)

    def __init__(
        self,
        ticker: str,
        value: str,
    ):
        self.ticker = ticker
        self.value = value

    def info(self):
        return {
            "sample_id": self.run_id,
            "ticker": self.ticker,
            "value": self.value,
        }
