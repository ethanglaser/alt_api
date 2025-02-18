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
from marshmallow import Schema, fields
# pprint library is used to make the output look more pretty
from pprint import pprint
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

class ArgsSchema(Schema):
    topic = fields.Str()
    sources = fields.List(fields.Str())

@index_blp.route('/test')
class Test(MethodView):
    """
    Hello world
    """
    @index_blp.arguments(ArgsSchema, location="query")
    @index_blp.response(HTTPStatus.OK, MessageSchema)  # return object
    def get(self, args) -> MessageSchema:
        """
        get request
        """
        print(args)
        # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
        client = MongoClient('mongodb+srv://umd3313:cornell@cluster0-e8xg6.mongodb.net/test?retryWrites=true&w=majority', tlsCAFile=certifi.where())
        database = client['AletheiaDataDesk']
        # Ukraine Russia
        topic_str = args['topic'] + " Inst"
        x = database.get_collection(topic_str)
        # example source list ["OJBBC", "OJFOX"]
        myquery = {'src': {'$in': args['sources']}}
        cursor = x.find(myquery)
        for document in cursor:
            print(document)
        #
        return MessageSchema().load({'message': 'testing api endpoint'})