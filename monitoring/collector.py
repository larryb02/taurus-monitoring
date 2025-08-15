from abc import ABC, abstractmethod
import logging
from pprint import pprint
import sys
import asyncio

import requests

import config


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)


class DataSource(ABC):
    """Describes a source to collect metrics from"""

    # Store source name, poll timer, and list of metrics to collect (add this once backend is setup)
    @abstractmethod
    def collect(self, endpoint):
        pass


class SystemMetricsSource(DataSource):
    """System Metrics"""

    def collect(self, endpoint):
        try:
            res = requests.get(f"{endpoint}/collect")
            return res.json()
        except Exception as e:
            logger.error(f"Failed to execute request: {e}")


class Node:
    def __init__(self, endpoint, poll_timer=3):
        self.endpoint = endpoint
        self.poll_timer = poll_timer
        self.datasource = (
            SystemMetricsSource()
        )  # only concerned with one statically assigned source for now

    async def _poll_node(self):
        """TODO: coroutine to periodically collect metrics"""
        while True:
            logger.debug(f"Collecting data for {self.endpoint}")
            try:
                pprint(self.datasource.collect(self.endpoint))
            except Exception as e:
                logger.error(f"Failed to collect metrics for {self.endpoint}: {e}")
            logger.debug(f"Polling again in {self.poll_timer}s")
            await asyncio.sleep(self.poll_timer)


class Collector:
    """Periodically collect metrics from datasource"""

    # Needs to be able to:
    # Collect data from static list of hosts
    # Communicate with Backend (Need to send collected data over to backend to perform db writes)

    def __init__(self):
        self.nodes = [
            Node(endpoint="http://localhost:8080", poll_timer=15)
        ]  # list of hosts to collect metrics on

    async def run(self):
        try:
            async with asyncio.TaskGroup() as tg:
                for node in self.nodes:
                    tg.create_task(node._poll_node())
        except KeyboardInterrupt:
            pass
        except ExceptionGroup as e:
            logger.error(f"Exception caught while polling node: {e}")
        except:
            sys.exit(3)


def main():
    c = Collector()
    try:
        asyncio.run(c.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
