from datetime import datetime as _datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from .base import Base


class Cache(Base):
    __tablename__ = "cache"

    id = Column(Integer, primary_key=True)

    ticker = Column(String)
    price = Column(Float)
    datetime = Column(DateTime)

    def __init__(
        self,
        ticker: str,
        price: float,
        datetime: _datetime = None,
    ):
        self.ticker = ticker
        self.price = price
        self.datetime = datetime or _datetime.now()

    def info(self):
        return {
            "ticker": self.ticker,
            "price": self.price,
            "datetime": self.datetime.isoformat(),
        }
