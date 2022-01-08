from __future__ import annotations
from datetime import datetime


from sqlalchemy import bindparam, create_engine, func, insert, select, update
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from .models.metric import Base, Jump, Run, Balance, Sample, Coin


class Metric:
    def __init__(self, path: str) -> None:
        self.path = path
        self.engine = create_engine(path)
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))
        Base.metadata.create_all(self.engine)
        self.session: Session = self.session_factory()

    def start_run(
        self,
        bridge: str,
        current_coin: str,
        scout_multiplier: float,
        scout_margin: float,
        use_margin: bool,
        interval_start: datetime,
        interval_end: datetime,
        run_start: datetime,
        run_end: datetime,
        coins: list[str]
    ) -> Run:
        entry = Run(
            bridge=bridge,
            current_coin=current_coin,
            scout_multiplier=scout_multiplier,
            scout_margin=scout_margin,
            use_margin=use_margin,
            interval_start=interval_start,
            interval_end=interval_end,
            run_start=run_start,
            run_end=run_end
        )
        for coin in coins:
            coin_entry = Coin(coin)
            entry.coins.append(coin_entry)

        self.session.add(entry)
        self.commit()
        return entry

    def end_run(self, run: Run):
        run.run_end = datetime.now()
        self.session.flush()
        self.session.commit()

    def jump(
        self,
        run: Run,
        ticker_from: str,
        ticker_to: str,
        ticker_from_quantity: float,
        ticker_to_quantity: float,
        ticker_from_value: float,
        ticker_to_value: float,
        ratio: float,
        datetime: datetime,
    ):
        entry = Jump(
            ticker_from=ticker_from,
            ticker_to=ticker_to,
            ticker_from_quantity=ticker_from_quantity,
            ticker_to_quantity=ticker_to_quantity,
            ticker_from_value=ticker_from_value,
            ticker_to_value=ticker_to_value,
            ratio=ratio,
            datetime=datetime,
        )
        run.jumps.append(entry)
    def sample(self, run: Run, date: datetime, btc_value: float, bridge_value: float):
        entry = Sample(btc_value, bridge_value, date)
        run.samples.append(entry)
        return entry

    def balance(self, sample: Sample, ticker: str, value: float):
        entry = Balance(ticker, value)
        sample.balances.append(entry)
        
    def commit(self):
        self.session.commit()    

    def flush(self):
        self.session.flush()

    def close(self):
        self.session.close()
