import logging

import psutil
from bottle import route, run

import agent.config as config


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)

"""
Tool for collecting and serving metrics over http
"""


def collect_metrics():
    metrics = {
        "cpu": {
            "cpu_usage": psutil.cpu_percent(),
            "cpu_freq": psutil.cpu_freq()._asdict(),
        },
        "mem": {
            "phys": psutil.virtual_memory()._asdict(),
            "swap": psutil.swap_memory()._asdict(),
        },
        "disk": [
            {part.mountpoint: psutil.disk_usage(part.mountpoint)._asdict()}
            for part in psutil.disk_partitions()
        ],
    }
    return metrics


@route("/collect")
def index():
    return collect_metrics()


if __name__ == "__main__":
    run()
