#!/usr/bin/env python3
"""
config file

reads configuration from environment
"""

from os import getenv
from dotenv import load_dotenv, find_dotenv
from typing import Optional
from loguru import logger

import utils.json_fix  # pylint: disable=unused-import

# database
MAIN_DB_CONNECTION_URI: str = ''

# api
API_TITLE: str = 'api'
API_VERSION: str = '3.0.1'
PORT: int = 8080

# misc
SECRET_KEY: str = ''
RECAPTCHA_SECRET: str = ''
JWT_ISSUER: str = 'issuer'
BASE_PATH: str = ''
DOCS_PATH: str = '/docs'
USE_RECAPTCHA: bool = True
PRODUCTION: bool = True
INSTALLATION_DIRECTORY: str = ''

CONFIG_LOADED: bool = False


def read_config() -> None:
    """
    read the config from environment
    """
    global MAIN_DB_CONNECTION_URI
    global API_TITLE
    global API_VERSION
    global CONFIG_LOADED
    global SECRET_KEY
    global RECAPTCHA_SECRET
    global JWT_ISSUER
    global BASE_PATH
    global DOCS_PATH
    global USE_RECAPTCHA
    global PORT
    global PRODUCTION
    global INSTALLATION_DIRECTORY

    if CONFIG_LOADED:
        logger.info('config already loaded')
        return

    load_dotenv(find_dotenv(usecwd=True), override=True)

    main_db_connection_uri: Optional[str] = MAIN_DB_CONNECTION_URI
    if main_db_connection_uri is None:
        raise ValueError('no main database connection uri provided')
    MAIN_DB_CONNECTION_URI = main_db_connection_uri

    api_title: Optional[str] = getenv('API_TITLE')
    if api_title is not None:
        API_TITLE = api_title
    api_version: Optional[str] = getenv('API_VERSION')
    if api_version is not None:
        API_VERSION = api_version
    port_str: Optional[str] = getenv('PORT')
    if port_str is not None:
        if not port_str.isdigit():
            raise ValueError(f'given port "{port_str}" is not an int')
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError(f'invalid port provided: {port}')
        PORT = port

    secret_key: Optional[str] = ''
    if secret_key is None:
        raise ValueError('no secret key provided')
    SECRET_KEY = secret_key

    recaptcha_secret: Optional[str] = ''
    if recaptcha_secret is None:
        raise ValueError('no recaptcha secret provided')
    RECAPTCHA_SECRET = recaptcha_secret

    jwt_issuer: Optional[str] = getenv('JWT_ISSUER')
    if jwt_issuer is not None:
        JWT_ISSUER = jwt_issuer

    base_path: Optional[str] = getenv('BASE_PATH')
    if base_path is not None:
        BASE_PATH = base_path
    docs_path: Optional[str] = getenv('DOCS_PATH')
    if docs_path is not None:
        DOCS_PATH = docs_path

    use_recaptcha: Optional[str] = getenv('USE_RECAPTCHA')
    if use_recaptcha is not None:
        USE_RECAPTCHA = use_recaptcha != 'false'

    production: Optional[str] = getenv('PRODUCTION')
    if production is not None:
        PRODUCTION = production == 'true'

    installation_directory: Optional[str] = ''
    if installation_directory is None:
        raise ValueError('no installation directory provided')
    INSTALLATION_DIRECTORY = installation_directory

    CONFIG_LOADED = True
    logger.info('config finished loading')


# you always want to run read_config on import, so there shouldn't be a run catch block
read_config()
