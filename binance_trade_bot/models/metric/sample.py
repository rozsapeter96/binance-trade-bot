from datetime import datetime as _datetime
from typing import ClassVar

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Float, Numeric
from sqlalchemy.orm import relationship


from .base import Base
from .run import Run


class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey("run.id"))
    btc_value = Column(Float)
    bridge_value = Column(Float)
    date = Column(DateTime)
    balances = relationship("Balance")

    def __init__(
        self,
        btc_value: float,
        bridge_value: float,
        date: _datetime = None,
    ):
        self.date = date or _datetime.now()
        self.btc_value = btc_value
        self.bridge_value = bridge_value

    def info(self):
        return {
            "run_id": self.run_id,
            "date": self.date,
            "btc_value": self.btc_value,
            "bridge_value": self.bridge_value
        }
