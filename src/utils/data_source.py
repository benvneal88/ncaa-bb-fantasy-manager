import sys
import os

import requests
import logging

from src.utils import logger as log_util


def download_file(url, file_path):
    logger = log_util.get_logger("data_source")
    logger.info(f"Downloading from {url} to file {file_path}")

    try:
        response = requests.get(url)
    except Exception as e:
        logger.error(e)
        logger.error(f"Failed to get web request: {url}")

    response.raise_for_status()

    with open(file_path, 'w') as file:
        file.write(response.content.decode("utf-8"))

