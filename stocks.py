#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Manage my portfolio of Robinhood stocks and automate buys and sells.
"""

from typing import Dict, Tuple

from pyrh import Robinhood
from influxdb import InfluxDBClient
from datetime import datetime
from json import loads, dumps
from time import sleep


class TheHood:
    """
    A wrapper for producing the kinds of transactions and calls on my Robinhood
    portfolio I'm looking for.
    """
    def __init__(self, credentials: str) -> None:
        self._rh = Robinhood()
        self._rh.login(**read_credentials(credentials))

    def total_dollar_equity(self) -> Tuple[float, float, float]:
        """
        Get values that explain the current monetary value of my account.

        Returns:
            A tuple containing today's closing equity in my account, followed by the
            previous day's closing value and the current extended / after-hours value.
        """
        return self._rh.equity(), self._rh.equity_previous_close(), self._rh.extended_hours_equity()

    def account_potential(self) -> float:
        """
        Get the total account potential for comparison against the total account value.
        I define account potential as the sum of all stocks' current worth plus the
        absolute value of any losses.

        Returns:
            A float representing the account potential.
        """
        stocks = self._rh.securities_owned()['results']
        potential_sum = 0.0
        for stock in stocks:
            # Make quantity a float as the API may change when I buy fractional shares.
            quantity = float(stock['quantity'])
            buy_price = float(stock['average_buy_price'])
            potential_sum += quantity * buy_price
        return potential_sum


def read_credentials(filename: str) -> Dict[str, str]:
    """
    Get the creds for an account from a JSON-formatted file.

    Args:
        filename: the file (with path) from which to read the credentials.

    Returns:
        The file's contents as a dictionary.
    """
    with open(filename, 'r') as fh:
        return loads(fh.read())


def publish_cache(js: dict, filename: str) -> None:
    """
    Publish some data to a cache file on the filesystem. This function would only need
    to be called if you were looking to call a publication request to the db from
    another program and you populated it here.

    Args:
        js: the data you wish to publish as JSON to the cache (must be of dict type).
        filename: the filename of the cache file to be updated.

    Returns:
        None, nothing.
    """
    # TODO: Since I'm actually going to publish this data right within Python via
    #       influxdb client, I'll skip this for now.
    pass


def main() -> None:
    th = TheHood(credentials='rh_credentials.json')
    influx_client = InfluxDBClient(**read_credentials('influxdb_credentials.json'))

    # Main loop.
    while True:
        potential = th.account_potential()
        today_close, prev_close, curr_val = th.total_dollar_equity()
        measurements = [
            {
                "measurement": "rh_portfolio",
                "tags": {
                    "vmhost": "1"
                },
                "time": datetime.utcnow().strftime(format='%Y-%m-%dT%H:%M:%S') + 'Z',
                "fields": {
                    "potential": round(potential, 2),
                    "today_close": round(today_close, 2),
                    "previous_close": round(prev_close, 2),
                    "current_value": round(curr_val, 2)
                }
            },
        ]
        print(dumps(measurements))
        influx_client.write_points(measurements)
        sleep(60)


if __name__ == '__main__':
    main()