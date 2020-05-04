#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Main entry point to my program at-current.

Cf. https://github.com/tensorflow/tensorflow/issues/35968#issuecomment-577017170 for
setting up the conda env.
"""


from stocks import TheHood
from influx import InfluxPublisher

from typing import Dict, Any, List, Union

from time import sleep
from datetime import datetime
from settings import env


measureT = List[Dict[str, Union[str, Dict[str, Union[Dict[str, float], str]]]]]


def package_measurements(name: str, fields: List[Dict[str, Any]], identifier: Dict[str, str]) -> measureT:
    """
    Package measurements in a list.

    Args:
        fields: the data to package as a series of measurements.

    Returns:

    """
    measurements = []
    for measures in fields:
        measurements.append(
            {
                "measurement": name,
                "tags": identifier,
                "time": datetime.utcnow().strftime(format='%Y-%m-%dT%H:%M:%S') + 'Z',
                "fields": measures
            }
        )
    return measurements


def main() -> None:
    th = TheHood(credentials=env['ROBINHOOD_CREDS'])

    # Main loop.
    while True:
        potential = th.account_potential()
        today_close, prev_close, curr_val = th.total_dollar_equity()

        with InfluxPublisher(env['INFLUXDB_CREDS']) as infpub:
            if curr_val != 0.0:
                infpub.publish(
                    package_measurements(
                        'rh_portfolio',
                        [
                            {
                                "potential": round(potential, 2),
                                "today_close": round(today_close, 2),
                                "previous_close": round(prev_close, 2),
                                "current_value": round(curr_val, 2)
                            }
                        ],
                        {'vmhost': '1'}
                    )
                )
            else:
                infpub.publish(
                    package_measurements(
                        'rh_portfolio',
                        [
                            {
                                "potential": round(potential, 2),
                                "today_close": round(today_close, 2),
                                "previous_close": round(prev_close, 2),
                                # Skip curr_val, or extended hours equity, until it's nonzero.
                            }
                        ],
                        {'vmhost': '1'}
                    )
                )

        sleep(env['SLEEP'])


if __name__ == '__main__':
    main()
