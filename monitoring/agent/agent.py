import logging
import os
import time
import sys

import psutil

import monitoring.config as config


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)

"""
Agent collects metrics and reports to collector
"""


def collect_metrics():
    metrics = {
        "cpu": {"cpu_usage": psutil.cpu_percent(), "cpu_freq": psutil.cpu_freq()},
        "mem": {"phys": psutil.virtual_memory(), "swap": psutil.swap_memory()},
        "disk": [
            psutil.disk_usage(part.mountpoint) for part in psutil.disk_partitions()
        ],
    }
    return metrics


def run():
    while True:
        print(collect_metrics())
        time.sleep(10)


if __name__ == "__main__":
    logger.info("Started agent")
    try:
        run()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
    logger.info("Shutdown agent")