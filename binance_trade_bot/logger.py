
from __future__ import annotations

import datetime
import logging.handlers
from typing import Dict

from .notifications import NotificationHandler
from .metric import Metric, Run

class Logger:

    Logger = None
    NotificationHandler = None

    def __init__(
        self,
        logging_service="crypto_trading",
        metric: Metric = None,
        enable_notifications=True,
    ):
        # Logger setup
        self.Logger = logging.getLogger(f"{logging_service}_logger")
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.propagate = False
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self.metric = metric
        self.active_run = None
        self.sample_counter = 0

        # default is "logs/crypto_trading.log"
        fh = logging.FileHandler(f"logs/{logging_service}.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.Logger.addHandler(fh)

        # logging to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.Logger.addHandler(ch)

        # notification handler
        self.NotificationHandler = NotificationHandler(enable_notifications)

    def close(self):
        for handler in self.Logger.handlers[:]:
            handler.close()

    def log(self, message, level="info", notification=True):

        if level == "info":
            self.Logger.info(message)
        elif level == "warning":
            self.Logger.warning(message)
        elif level == "error":
            self.Logger.error(message)
        elif level == "debug":
            self.Logger.debug(message)

        if notification and self.NotificationHandler.enabled:
            self.NotificationHandler.send_notification(str(message))

    def info(self, message, notification=True):
        self.log(message, "info", notification)

    def warning(self, message, notification=True):
        self.log(message, "warning", notification)

    def error(self, message, notification=True):
        self.log(message, "error", notification)

    def debug(self, message, notification=False):
        self.log(message, "debug", notification)

    def jump_metric(
        self,
        ticker_from: str,
        ticker_to: str,
        ticker_from_quantity: float,
        ticker_to_quantity: float,
        ticker_from_value: float,
        ticker_to_value: float,
        ratio: float,
        datetime: datetime,
    ):
        if self.metric is not None:
            self.metric.jump(
                self.active_run,
                ticker_from,
                ticker_to,
                ticker_from_quantity,
                ticker_to_quantity,
                ticker_from_value,
                ticker_to_value,
                ratio,
                datetime,
            )

    def start_run_metric(
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
        if self.metric is not None:
            run = self.metric.start_run(
                bridge,
                current_coin,
                scout_multiplier,
                scout_margin,
                use_margin,
                interval_start,
                interval_end,
                run_start,
                run_end,
                coins
            )
            self.active_run = run
            return run

    def end_run_metric(self, run: Run):
        if self.metric is not None:
            self.metric.end_run(run)
            self.active_run = None

    def balance_metric(self, run: Run, balances: Dict[str, float],date: datetime, btc_value: float, bridge_value: float):
        if self.metric is not None:
            self.sample_counter = self.sample_counter + 1
            sample = self.metric.sample(run, date, btc_value, bridge_value)
            for ticker, value in balances.items():
                self.metric.balance(sample, ticker, value)
            if self.sample_counter % 5 == 0:
                self.metric.commit()
