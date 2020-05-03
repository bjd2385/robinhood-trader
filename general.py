"""
General utility functions and classes.
"""

from typing import Dict

from json import loads


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
