#! /usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Main entry point to my program at-current.

Cf. https://github.com/tensorflow/tensorflow/issues/35968#issuecomment-577017170 for
setting up the conda env.
"""


from stocks import TheHood
from influx import InfluxPublisher, DaemonInfluxPublisher

from typing import Dict, Any, List, Union

from time import sleep
from datetime import datetime, timedelta
from settings import env


measureT = List[Dict[str, Union[str, Dict[str, Union[Dict[str, float], str]]]]]


def package_measurements(name: str, fields: List[Dict[str, Any]], identifier: Dict[str, str]) -> measureT:
    """
    Package measurements in a list.

    Args:
        name: the name of the time series of which to publish the data points.
        fields: the data to package as a series of measurements.
        identifier: additional tags to add to the measurements.

    Returns:
        A measureT-type / structured object for publication to an Influxdb.
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
    with DaemonInfluxPublisher(env['INFLUXDB_CREDS']) as infpub:
        while True:
            potential = th.account_potential()
            today_close, prev_close, curr_val = th.total_dollar_equity()

            # Get the total dividend payment sum for the past year.
            dividend_sum = th.dividend_payments(since=datetime.isoformat(datetime.now() - timedelta(days=365)))
            
            if curr_val != 0.0:
                infpub.publish(
                    package_measurements(
                        'rh_portfolio',
                        [
                            {
                                "potential": round(potential, 2),
                                "today_close": round(today_close, 2),
                                "previous_close": round(prev_close, 2),
                                "current_value": round(curr_val, 2),
                                "dividend_payment_sum": round(dividend_sum, 2)
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
                                "dividend_payment_sum": round(dividend_sum, 2)
                            }
                        ],
                        {'vmhost': '1'}
                    )
                )

            sleep(env['SLEEP'])


if __name__ == '__main__':
    main()
