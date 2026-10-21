import json
import psycopg
from src.connection import get_connection
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_json_file(filepath):
    logger.info('Reading file...')
    with open(filepath) as f:
        for row in json.load(f):
            yield row
    logger.info('File read!')
