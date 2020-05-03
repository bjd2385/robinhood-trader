"""
Load environment variables via dotenv.
"""

import os

from dotenv import load_dotenv


load_dotenv()

__all__ = [
    'env'
]

env = {
    'THUNDERBIRD_CONF': os.getenv('THUNDERBIRD_CONF'),
    'ROBINHOOD_CREDS': os.getenv('ROBINHOOD_CREDS'),
    'INFLUXDB_CREDS': os.getenv('INFLUXDB_CREDS')
}