"""
Handle the Influxdb transactions and publications that need to occur.
"""

from general import read_credentials

from typing import List, Dict, Union, Any

from influxdb import InfluxDBClient
from contextlib import AbstractContextManager


measureT = List[Dict[str, Union[str, Dict[str, Union[Dict[str, float], str]]]]]


class InfluxPublisher(AbstractContextManager):
    def __init__(self, credentials: str) -> None:
        self._client = InfluxDBClient(**read_credentials(credentials))

    def publish(self, js: measureT, retry_delay: int =10) -> None:
        """
        Publish a metric to the configured Influx DB.

        Args:
            js: the data to publish (a list of measurements).

        Returns:
            Nothing.
            TODO: If the publication does not succeed, implement a 'try-again' in like 10s.

        Raises:
            # TODO: better-define the exception that is thrown until the implementation of
            #       a retry on failure is added.
        """
        # TODO: correct implementation of failed try on publish.
        print(js)
        self._client.write_points(js)

    def __enter__(self) -> 'InfluxPublisher':
        return self

    def __exit__(self, *args: Any) -> None:
        self._client.close()
