from datetime import datetime as datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, Numeric
from sqlalchemy.orm import relation, relationship

from .base import Base


class Run(Base):
    __tablename__ = "run"

    id = Column(Integer, primary_key=True)
    interval_start = Column(DateTime)
    interval_end = Column(DateTime)
    run_start = Column(DateTime)
    run_end = Column(DateTime)
    bridge = Column(String)
    current_coin = Column(String)
    scout_multiplier = Column(Numeric)
    scout_margin = Column(Numeric)
    use_margin = Column(Boolean)
    jumps = relationship("Jump")
    samples = relationship("Sample")
    coins = relationship("Coin")


    def __init__(
        self,
        bridge: str,
        current_coin: str,
        scout_multiplier: float,
        scout_margin: float,
        use_margin: bool,
        interval_start: datetime = None,
        interval_end: datetime = None,
        run_start: datetime = None,
        run_end: datetime = None,
    ):
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.run_start = run_start
        self.run_end = run_end
        self.bridge = bridge
        self.current_coin = current_coin
        self.scout_multiplier = scout_multiplier
        self.scout_margin = scout_margin
        self.use_margin = use_margin

    def info(self):
        return {
            "interval_start": self.interval_start.isoformat(),
            "interval_end": self.interval_end.isoformat(),
            "run_start": self.run_start.isoformat(),
            "run_end": self.run_end.isoformat(),
            "bridge": self.bridge,
            "current_coin": self.current_coin,
            "scout_multiplier": self.scout_multiplier,
            "scout_margin": self.scout_margin,
            "use_margin": self.use_margin
        }
