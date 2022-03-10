#!/usr/bin/env python3
"""
auth functionality
"""

import jwt
from flask_cors import CORS
from flask.views import MethodView
from marshmallow import Schema, fields, post_load
from marshmallow.validate import Length
from peewee import DoesNotExist
from typing import Optional, Dict, Any
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_smorest import Blueprint, abort
from marshmallow_enum import EnumField
from http import HTTPStatus

from auth.recaptcha import verify_recaptcha
from auth.shared import JWTAuthData
from models.users import Users
from utils.config import SECRET_KEY, BASE_PATH, USE_RECAPTCHA
from utils.enums import UserType

auth_blp = Blueprint(
    'authentication', 'authentication', url_prefix=f'{BASE_PATH}/auth',
    description='Operations on users'
)
CORS(auth_blp)


class LoginArgs:
    """
    login args
    """

    def __init__(self, usernameEmail: str, password: str, recaptchaToken: str) -> None:
        self.usernameEmail = usernameEmail
        self.password = password
        self.recaptchaToken = recaptchaToken


class LoginArgsSchema(Schema):
    """
    login args
    """
    usernameEmail = fields.String(required=True, description="usernameEmail", validate=Length(
        min=1, error="no username provided"))
    password = fields.String(required=True, description="password", validate=Length(
        min=1, error="no password provided"))
    recaptchaToken = fields.String(
        required=True, description="login recaptcha token")

    @post_load
    def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> LoginArgs:
        """
        create object initialization
        """
        return LoginArgs(**data)


class LoginRes:
    """
    login res object
    """

    def __init__(self, token: str, user_type: UserType, id: str) -> None:  # pylint: disable=redefined-builtin
        self.token = token
        self.user_type = user_type
        self.id = id


class LoginResSchema(Schema):
    """
    login res object schema
    """
    token = fields.String(required=True, description="result token")
    user_type = EnumField(UserType, required=True, description="user type")
    id = fields.UUID(required=True, description="user id")

    @post_load
    def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> LoginRes:
        """
        create object initialization
        """
        return LoginRes(**data)


@auth_blp.route('/login')
class Login(MethodView):
    """
    user login
    """

    @auth_blp.arguments(LoginArgsSchema)
    @auth_blp.response(HTTPStatus.OK, LoginResSchema)
    def post(self, args: LoginArgs):
        """
        post request
        """
        if USE_RECAPTCHA:
            verify_recaptcha(args.recaptchaToken)
        user_data: Optional[Users] = None
        try:
            if '@' in args.usernameEmail:
                user_data = Users.select(Users.id, Users.user_type, Users.password).where(
                    Users.email == args.usernameEmail).get()
            else:
                user_data = Users.select(Users.id, Users.user_type, Users.password).where(
                    Users.username == args.usernameEmail).get()
        except DoesNotExist:
            abort(HTTPStatus.NOT_FOUND,
                  message='cannot find user with given username / email')
            return None

        assert user_data is not None
        hasher = PasswordHasher()
        try:
            hasher.verify(user_data.password, args.password)
        except VerifyMismatchError:
            abort(HTTPStatus.UNAUTHORIZED, message='password is invalid')
            return None

        auth_data = JWTAuthData(user_data.id.hex, user_data.user_type)
        token = jwt.encode(vars(auth_data), SECRET_KEY, algorithm='HS256')

        return LoginResSchema().load({'token': token, 'user_type': user_data.user_type, 'id': user_data.id})
