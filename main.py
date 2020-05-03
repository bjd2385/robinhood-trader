#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from stocks import TheHood
from influx import InfluxPublisher

from time import sleep
from datetime import datetime
from settings import env


def main() -> None:
    th = TheHood(credentials=env['ROBINHOOD_CREDS'])

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

        with InfluxPublisher(env['INFLUXDB_CREDS']) as infpub:
            infpub.publish(measurements)

        sleep(60)


if __name__ == '__main__':
    main()
