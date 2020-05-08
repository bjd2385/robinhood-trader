"""
Manage my portfolio of Robinhood stocks and automate buys and sells.
"""

from general import read_credentials

from typing import Tuple, Union, Callable, Any

from pyrh import Robinhood
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from functools import wraps


__all__ = [
    'TheHood',
]


def retry(f: Callable, tries: int =3, debug: bool =True) -> Callable:
    """
    Retry a Robinhood requests-based call after getting 500s.

    Args:
        f: the method we're to decorate and retry.
        tries: the number of attempts to make at logging back in before we simply
               give up until the next iteration.
        debug: print information about the errors received on requests.

    Returns:
        The same method called after logging back into the Robinhood API.
    """
    @wraps(f)
    def new_f(*args: Any, **kwargs: Any) -> Any:
        for _ in range(tries):
            try:
                return f(*args, **kwargs)
            except HTTPError:
                if debug:
                    print('Robinhood request failed, retrying')
            except JSONDecodeError:
                if debug:
                    print('Robinhood request did not see appropriate JSON, retrying')
    return new_f


class TheHood:
    """
    A wrapper for producing the kinds of transactions and calls on my Robinhood
    portfolio I'm looking for.
    """
    def __init__(self, credentials: str) -> None:
        self._ext_equity = 0.0

        # Set up connection to Robinhood's API.
        self._rh = Robinhood()
        self._rh.login(**read_credentials(credentials))

    @property
    def extended_hours_equity(self) -> float:
        """
        Keep track of the extended equity and prevent its setting to NoneType.

        Returns:
            The current extended equity.
        """
        return self._ext_equity

    @extended_hours_equity.setter
    def extended_hours_equity(self, new_equity: Union[float, None]) -> None:
        """
        Keep track of the extended equity and prevent its setting to NoneType.

        Returns:
            The current extended equity.
        """
        if type(new_equity) is not float:
            pass
        else:
            self._ext_equity = new_equity

    @retry
    def total_dollar_equity(self) -> Tuple[float, float, float]:
        """
        Get values that explain the current monetary value of my account.

        Returns:
            A tuple containing today's closing equity in my account, followed by the
            previous day's closing value and the current extended / after-hours value.
        """
        self.extended_hours_equity = self._rh.extended_hours_equity()
        return self._rh.equity(), self._rh.equity_previous_close(), self.extended_hours_equity

    @retry
    def account_potential(self) -> float:
        """
        Get the total account potential for comparison against the total account value.
        I define account potential as the sum of all stocks' current worth plus the
        absolute value of any losses.

        Returns:
            A float representing the account potential.
        """
        stocks = self._rh.securities_owned()['results']
        potential_sum = float(self._rh.portfolios()['withdrawable_amount'])
        for stock in stocks:
            # Make quantity a float as the API may change when I buy fractional shares.
            quantity = float(stock['quantity'])
            buy_price = float(stock['average_buy_price'])
            potential_sum += quantity * buy_price
        return potential_sum
