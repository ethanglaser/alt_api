#!/usr/bin/env python3
"""
index handler
"""
from flask_cors import CORS
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields, post_load
from marshmallow.validate import Length
from utils.config import BASE_PATH
from http import HTTPStatus
from typing import Dict, Any

database_blp = Blueprint(
    'database', 'database', url_prefix=f'{BASE_PATH}/database',
    description='Index route'
)

CORS(database_blp)

class DatabaseArgs:
    """
    database args
    """

    def __init__(self, user_id: str, topic: str) -> None:
        self.user_id = user_id
        self.topic = topic

class DatabaseArgsSchema(Schema):
    """
    database args
    """
    user_id = fields.String(required=True, description="user id", validate=Length(
        min=1, error="no user id"))
    topic = fields.String(required=True, description="topic", validate=Length(
        min=1, error="no topic"))

    @post_load
    def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> DatabaseArgs:
        """
        create object initialization
        """
        return DatabaseArgs(**data)

class DatabaseRes:
    """
    database res object
    """

    def __init__(self, score: float) -> None:
        self.score = score


class DatabaseResSchema(Schema):
    """
    login res object schema
    """
    score = fields.Float(required=True, description="similarity score")

    @post_load
    def make_object(self, data: Dict[str, Any], **_kwargs: Any) -> DatabaseRes:
        """
        create object initialization
        """
        return DatabaseRes(**data)


@database_blp.route('/')
class Index(MethodView):
    """
    Test database call page
    """
    @database_blp.arguments(DatabaseArgsSchema)
    @database_blp.response(HTTPStatus.OK, DatabaseResSchema)
    def post(self, args: DatabaseArgs) -> DatabaseResSchema:
        """
        post request
        """
        return DatabaseResSchema().load({'score': 1.0})
