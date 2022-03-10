#!/usr/bin/env python3
"""
get user data
"""

from flask_cors import CORS
from flask.views import MethodView
from marshmallow import Schema, fields, post_load, EXCLUDE
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict
from typing import Optional, Dict, Any
from flask_smorest import Blueprint, abort
from marshmallow_enum import EnumField
from http import HTTPStatus

from models.users import Users
from utils.middleware import require_login
from utils.config import BASE_PATH
from utils.enums import UserType

users_blp = Blueprint(
    'users', 'users', url_prefix=f'{BASE_PATH}/users',
    description='Operations on users'
)
CORS(users_blp)


class PublicUserRes:
    """
    public user res object
    """

    def __init__(self, id: int, email: str, username: str, name: str, user_type: UserType) -> None:  # pylint: disable=redefined-builtin
        self.id = id
        self.email = email
        self.username = username
        self.name = name
        self.user_type = user_type


# should match user in sdk
class PublicUserResSchema(Schema):
    """
    user res object schema
    """
    id = fields.UUID(required=True, description="user id")
    email = fields.String(required=True, description="user email")
    username = fields.String(required=True, description="username")
    name = fields.String(required=True, description="user name")
    user_type = EnumField(UserType, required=True, description="user type")

    @post_load
    def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> PublicUserRes:
        """
        create object initialization
        """
        return PublicUserRes(**data)

    class Meta:
        """
        schema config
        """
        unknown = EXCLUDE


@users_blp.route('/<string:user_id>')
class UserRoute(MethodView):
    """
    user data
    """

    @users_blp.response(HTTPStatus.OK, PublicUserResSchema)
    @require_login
    def get(self, user_id: int):
        """
        get request
        """
        user: Optional[Users] = None
        try:
            user = Users.select().where(Users.id == user_id).get()
        except DoesNotExist:
            abort(HTTPStatus.NOT_FOUND,
                  message=f'cannot find user with id {user_id}')

        return PublicUserResSchema().load(model_to_dict(user))


@users_blp.route('/')
class UsersRoute(MethodView):
    """
    user data
    """

    @users_blp.response(HTTPStatus.OK, PublicUserResSchema(many=True))
    @require_login
    def get(self):
        """
        get request
        """
        users = Users.select()
        return [PublicUserResSchema().load(model_to_dict(user)) for user in users]
