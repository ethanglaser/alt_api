#!/usr/bin/env python3
"""
flask middleware
"""
import jwt
from json import dumps
from flask_smorest import abort
from typing import Any
from datetime import timedelta
from http import HTTPStatus
from flask import g, request
from uuid import UUID
from utils.config import SECRET_KEY
from auth.shared import JWTAuthDataSchema
from marshmallow.exceptions import ValidationError
from functools import wraps
from urllib.parse import urlencode

DEFAULT_CACHE_TIME: timedelta = timedelta(minutes=20)


def get_auth() -> None:
    '''
    gets the authentication information
    '''
    if 'auth' in g:
        return

    auth_header = request.headers.get('authorization')
    if auth_header is None:
        return
    if 'Bearer' not in auth_header:
        abort(HTTPStatus.BAD_REQUEST, message='no bearer found')
    split_str = auth_header.split('Bearer ')
    if len(split_str) < 2:
        abort(HTTPStatus.BAD_REQUEST, message='invalid bearer token provided')

    raw_jwt = split_str[1]
    try:
        auth_data_dict = jwt.decode(raw_jwt, SECRET_KEY, algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        abort(HTTPStatus.BAD_REQUEST, message="error decoding jwt")
    try:
        auth_data_dict['id'] = UUID(auth_data_dict['id'])
        auth_data = JWTAuthDataSchema().load(auth_data_dict)
        g['auth'] = auth_data
    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, message="invalid jwt provided")


def require_login(f):
    """
    require user to be logged in (decorator)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs: Any):
        if g.get('auth') is None:
            abort(HTTPStatus.UNAUTHORIZED, message="user not logged in")
        return f(*args, **kwargs)
    return decorated_function


def get_query_params() -> str:
    """
    get query params from given request
    """
    args = request.args
    query_params = urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return query_params


def get_json_params() -> str:
    """
    get josn body params for given request
    """
    json_data = request.json
    if json_data is None:
        return ''
    request_data = dumps(json_data, sort_keys=True)
    return request_data
