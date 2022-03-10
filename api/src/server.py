#!/usr/bin/env python3
"""
flask server
"""

import logging
from flask import Flask
from flask_cors import CORS
from os.path import join
from loguru import logger
from flask_smorest import Api
from http import HTTPStatus
from flask_smorest.error_handler import ErrorSchema

from utils.main import relative_file_path

from utils.config import SECRET_KEY, BASE_PATH, DOCS_PATH, API_TITLE, API_VERSION, PRODUCTION
from utils.middleware import get_auth
from misc.index import index_blp
from database_call.index import database_blp
from auth.auth import auth_blp
from auth.users import users_blp


class InterceptHandler(logging.Handler):
    """
    use for loguru logger
    """

    def emit(self, record) -> None:
        """
        send to loguru
        """
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def http_error_handler(error: Exception):
    """
    unhandled error handler
    """
    logger.exception(error)
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    return ErrorSchema().load({'message': str(error), 'code': code}), code


def build_server() -> Flask:
    """
    initializes flask server
    """
    app = Flask(API_TITLE)

    # register loguru as handler
    logger_handler = InterceptHandler()
    logger_handler.setLevel(0)
    app.logger.addHandler(logger_handler)  # pylint: disable=no-member
    logging.basicConfig(handlers=[logger_handler])

    app.register_error_handler(Exception, http_error_handler)

    app.secret_key = SECRET_KEY

    app.config.from_object(__name__)

    app.config.update({
        'API_TITLE': API_TITLE,
        'API_VERSION': API_VERSION,
        'OPENAPI_VERSION': '3.0.3',
        'OPENAPI_JSON_PATH': 'spec.json',
        'OPENAPI_URL_PREFIX': BASE_PATH + DOCS_PATH,
        'OPENAPI_REDOC_PATH': '/redoc',
        'OPENAPI_REDOC_URL': 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js',
        'OPENAPI_SWAGGER_UI_PATH': '/swagger-ui',
        'OPENAPI_SWAGGER_UI_URL': 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/',
    })

    # cors
    # also needs to go on each blueprint
    CORS(app)

    api = Api(app)

    # add jwt bearer auth to swagger
    api.spec.components.security_scheme(
        "bearerAuth", {"type": "http",
                       "scheme": "bearer", "bearerFormat": "JWT"}
    )
    api.spec.options["security"] = [{"bearerAuth": []}]

    # middleware

    app.before_request(get_auth)

    # routes

    api.register_blueprint(index_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(database_blp)

    # generate swagger file

    base_folder: str = '/tmp' if PRODUCTION else '.'
    with open(relative_file_path(join(base_folder, 'swagger.yml')), 'w', encoding='utf8') as swagger_file:
        swagger_file.write(api.spec.to_yaml())

    return app
