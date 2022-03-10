#!/usr/bin/env python3
"""
Utils helper functions
"""

from os.path import abspath, join
from loguru import logger
from urllib.parse import urlparse
from peewee import PostgresqlDatabase

from utils.config import INSTALLATION_DIRECTORY


def normalize_str(name: str) -> str:
    """
    return normalized string for paths and such
    """
    return name.strip().replace(' ', '_').lower()


def relative_file_path(rel_path: str) -> str:
    """
    get file path relative to current directory
    """
    complete_path: str = join(abspath(INSTALLATION_DIRECTORY), rel_path)
    return complete_path


def get_database(uri: str) -> PostgresqlDatabase:
    """
    parse uri and get database object
    """
    logger.info('opening database')
    connection_config = urlparse(uri)
    database_name = connection_config.path.replace('/', '')
    logger.info(f'database name: {database_name}')
    database_connection = PostgresqlDatabase(database_name, user=connection_config.username, password=connection_config.password,
                                             host=connection_config.hostname, port=connection_config.port, autorollback=True)
    logger.info(f'created connection to {database_name}')
    return database_connection