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
    'SLEEP': int(os.getenv('SLEEP'))
}
