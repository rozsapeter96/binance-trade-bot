from datetime import datetime as _datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from .base import Base
from .run import Run


class Jump(Base):
    __tablename__ = "jump"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.id"))
    ticker_from = Column(String)
    ticker_to = Column(String)
    ticker_from_quantity = Column(Numeric)
    ticker_to_quantity = Column(Numeric)
    ticker_from_value = Column(Numeric)
    ticker_to_value = Column(Numeric)
    date = Column(DateTime)
    ratio = Column(Numeric)

    def __init__(
        self,
        ticker_from: str,
        ticker_to: str,
        ticker_from_quantity: float,
        ticker_to_quantity: float,
        ticker_from_value: float,
        ticker_to_value: float,
        ratio: float,
        datetime: _datetime = None,
    ):
        self.ticker_from = ticker_from
        self.ticker_to = ticker_to
        self.ticker_from_quantity = ticker_from_quantity
        self.ticker_to_quantity = ticker_to_quantity
        self.ticker_from_value = ticker_from_value
        self.ticker_to_value = ticker_to_value
        self.ratio = ratio
        self.date = datetime or _datetime.now()

    def info(self):
        return {
            "run_id": self.run_id,
            "ticker_from": self.ticker_from,
            "ticker_to": self.ticker_to,
            "ticker_from_quantity": self.ticker_from_quantity,
            "ticker_to_quantity": self.ticker_to_quantity,
            "ticker_from_value": self.ticker_from_value,
            "ticker_to_value": self.ticker_to_value,
            "ratio": self.ratio,
            "datetime": self.datetime.isoformat(),
        }
