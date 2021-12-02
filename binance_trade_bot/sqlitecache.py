from datetime import datetime, timedelta
from sqlalchemy.sql.sqltypes import Date, Numeric, String


from sqlalchemy import bindparam, create_engine, func, insert, select, update
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from contextlib import contextmanager, nullcontext
from .models.cache import Cache


class SQLiteCache():
    def __init__(self, path: str) -> None:
        self.memcache = dict()
        self.path = path
        self.engine = create_engine(path)
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))
        Cache.metadata.create_all(self.engine)
        self.session: Session = self.session_factory()
        
    def get(self, ticker: str, date: datetime) -> Cache:
        if(ticker not in self.memcache or date not in self.memcache[ticker]):
            entries = self.session.query(Cache).filter(Cache.ticker == ticker, Cache.datetime >=  date, Cache.datetime <= date + timedelta(minutes=999)).all()
            self.memcache[ticker] = dict((entry.datetime, entry) for entry in entries)
        
        return self.memcache[ticker].get(date, None)
    def add(self, ticker: str, date: datetime, value: float):
        entry = Cache(ticker = ticker, datetime = date, price = value)
        self.session.add(entry)
    def commit(self):
        self.session.commit()
    def close(self):
        self.session.close()
