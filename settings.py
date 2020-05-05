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
    'ROBINHOOD_CREDS': os.getenv('ROBINHOOD_CREDS'),
    'INFLUXDB_CREDS': os.getenv('INFLUXDB_CREDS'),
    # Bulbea market sentiment analysis via Twitter.
    'BULBEA_TWITTER_API_KEY': os.getenv('BULBEA_TWITTER_API_KEY'),
    'BULBEA_TWITTER_API_SECRET': os.getenv('BULBEA_TWITTER_API_SECRET'),
    'BULBEA_TWITTER_ACCESS_TOKEN': os.getenv('BULBEA_TWITTER_ACCESS_TOKEN'),
    'BULBEA_TWITTER_ACCESS_TOKEN_SECRET': os.getenv('BULBEA_TWITTER_ACCESS_TOKEN_SECRET'),
    # Main loop sleep.
    'SLEEP': int(os.getenv('SLEEP')),
    # Daemon configuration.
    'DAEMON_WAKEUP': int(os.getenv('DAEMON_WAKEUP')),
    'QUEUE_MAX': int(os.getenv('QUEUE_SIZE')),
    'TIMEOUT': int(os.getenv('QUEUE_TIMEOUT')),
    'MAX_THREADS': int(os.getenv('MAX_THREADS')),
    'QUEUE_TIMEOUT': int(os.getenv('QUEUE_TIMEOUT'))
}
