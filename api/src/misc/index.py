#!/usr/bin/env python3
"""
index handler
"""
from flask_cors import CORS
from flask.views import MethodView
from flask_smorest import Blueprint
from utils.message_object import MessageSchema
from utils.config import BASE_PATH, DOCS_PATH
from http import HTTPStatus
from pymongo import MongoClient
import certifi


index_blp = Blueprint(
    'misc', 'index', url_prefix=BASE_PATH,
    description='Index route'
)

CORS(index_blp)


@index_blp.route('/')
class Index(MethodView):
    """
    Default api page
    """
    @index_blp.response(HTTPStatus.OK, MessageSchema)  # return object
    def get(self) -> MessageSchema:
        """
        get request
        """
        return MessageSchema().load({'message': f'go to {BASE_PATH}{DOCS_PATH}/swagger-ui or {BASE_PATH}{DOCS_PATH}/redoc to view the swagger docs'})


@index_blp.route('/hello')
class Hello(MethodView):
    """
    Hello world
    """
    @index_blp.response(HTTPStatus.OK, MessageSchema)  # return object
    def get(self) -> MessageSchema:
        """
        get request
        """
        client = MongoClient(
            'mongodb+srv://umd3313:cornell@cluster0-e8xg6.mongodb.net/test?retryWrites=true&w=majority', tlsCAFile=certifi.where())
        db = client.admin
        database = client['AletheiaDataDesk']
        x = database.get_collection("BTC & ETH Stats")
        print(x.find_one())
        return MessageSchema().load({'message': 'hello world'})
