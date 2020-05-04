"""
Handle the Influxdb transactions and publications that need to occur.
"""

from general import read_credentials
from settings import env

from typing import List, Dict, Union, Any

from influxdb import InfluxDBClient
from contextlib import AbstractContextManager
from queue import Queue
from threading import Thread
from time import sleep


measureT = List[Dict[str, Union[str, Dict[str, Union[Dict[str, float], str]]]]]


class InfluxPublisher(AbstractContextManager):
    """
    Manage the publication of data points to Influxdb.
    """
    def __init__(self, credentials: str) -> None:
        self._client = InfluxDBClient(**read_credentials(credentials))

    def publish(self, js: measureT) -> None:
        """
        Publish a metric to the configured Influx DB.

        Args:
            js: the data to publish (a list of measurements).

        Returns:
            Nothing.
        """
        self._client.write_points(js)

    def __enter__(self) -> 'InfluxPublisher':
        return self

    def __exit__(self, *args: Any) -> None:
        self._client.close()


class DaemonInfluxPublisher:
    """
    Provide an interface to a daemon that periodically flushes a queue of data points.
    """
    def __init__(self, credentials: str) -> None:
        self.queue = Queue(maxsize=env['QUEUE_MAX'])

        # Start a non-blocking daemon thread that's created and periodically reads
        # from the queue, as well as spins up additional threads.
        self._publish_daemon = Thread(target=self._d_publisher, daemon=True)
        self._publish_daemon.start()

        # Create a client connection, with which we intend to publish measurements.
        self._client = InfluxDBClient(**read_credentials(credentials))

    def publish(self, js: measureT) -> None:
        """
        Add a metric to the queue for the daemon to flush periodically. I've kept the
        interface the same as `publish` on `InfluxPublisher`, above.

        Args:
            js: the data to publish (a list of measurements).

        Returns:
            Nothing.
        """
        self.queue.put(js, timeout=env['QUEUE_TIMEOUT'])

    def _d_publisher(self) -> None:
        """
        'Daemonized' publisher that has the ability to spin up other threads.
        Periodically wakes up and tries to empty its queue of measurements.

        Returns:
            Nothing.
        """
        def t_publish(p: measureT) -> None:
            self._client.write_points(p)

        while True:
            if not self.queue.empty():
                print(self.queue.qsize())
                # No reason to create more threads than necessary, here.
                if env['MAX_THREADS'] > self.queue.qsize():
                    n_threads = self.queue.qsize()
                    mod = 1
                else:
                    n_threads = env['MAX_THREADS']
                    mod = self.queue.qsize() % n_threads

                # TODO: figure out what to do with remainder
                # Try to drain the entire queue of measurements.
                for _ in range(mod):
                    threads = []
                    for _ in range(n_threads):
                        measurements = self.queue.get()
                        new_thread = Thread(target=t_publish, args=(measurements,), daemon=False)
                        new_thread.start()
                        threads.append(new_thread)
                    print(threads)
                    for thread in threads:
                        thread.join()
            print('Daemon loop')
            sleep(env['DAEMON_WAKEUP'])

    def __enter__(self) -> 'DaemonInfluxPublisher':
        return self

    def __exit__(self, *args: Any) -> None:
        # TODO: figure out the correct way to kill the daemon safely?
        pass
