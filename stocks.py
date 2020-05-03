"""
Manage my portfolio of Robinhood stocks and automate buys and sells.
"""

from general import read_credentials

from typing import Tuple

from pyrh import Robinhood


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
