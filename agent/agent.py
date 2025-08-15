import logging
import argparse

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


def main():
    parser = argparse.ArgumentParser(
        prog="Metrics Agent",
        description="Export system metrics over http",
        epilog="yo gurt --help",
    )
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("-q", "--quiet", action="store_true", default=False)

    args = parser.parse_args()
    logger.debug(f"Parsed Args: {args}")
    agent_config = vars(args)
    logger.debug(f"Running with config {agent_config}")
    run(**agent_config)


if __name__ == "__main__":
    main()
