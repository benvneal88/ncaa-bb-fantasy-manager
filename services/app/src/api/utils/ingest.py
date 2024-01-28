import os
import requests

import api.utils.logger as log_util

logger = log_util.get_logger("ingest")


def download_file(url, file_path):
    logger.info(f"Downloading from {url} to file {file_path}")

    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        logger.debug(f"\tcreating folder path {dir_path}")
        os.makedirs(dir_path)

    try:
        response = requests.get(url)
    except Exception as e:
        logger.error(e)
        logger.error(f"Failed to get web request: {url}")

    response.raise_for_status()

    with open(file_path, 'w') as file:
        file.write(response.content.decode("utf-8"))

