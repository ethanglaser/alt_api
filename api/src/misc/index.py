#!/usr/bin/env python3
"""
index handler
"""
from encodings import utf_8
from flask_cors import CORS
from flask.views import MethodView
from flask_smorest import Blueprint
from utils.message_object import MessageSchema
from utils.config import BASE_PATH, DOCS_PATH
from http import HTTPStatus
from pymongo import MongoClient
import certifi
from pprint import pprint
import pandas as pd
from marshmallow import Schema, fields


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


def doclist_to_output_original(doclist):
    pre_csv = {'text': [], 'date': [], 'source': [], 'group_id': []}
    for doc in doclist:
        # insert if statement here to filter out some of the docs
        if 'inst' in doc.keys() and len(doc['inst']) and 'text' in doc['inst'][0].keys():
            pre_csv['text'].append(doc['inst'][0]['text'])
        else:
            pre_csv['text'].append('')
        pre_csv['date'].append(doc['beg']) #same as end? convert to datetime?
        pre_csv['source'].append(doc['src']) # or doc['srcc'][0]['srcs'][0]['src'] if stats like object
        print(doc['uid'])
        pre_csv['group_id'].append(doc['uid'])

    df = pd.DataFrame(pre_csv)
    df.to_csv("sample_csv.csv", index=False)
    return df

def doclist_to_output(doclist):
    pre_csv = {'text': [], 'date': [], 'path': [], 'group_id': []}
    for doc in doclist:
        print(1)
        for doc_inst in doc['inst']:
            for key in doc_inst.keys():
                if key == 'text':
                    pre_csv['text'].append(doc_inst['text'])
                elif key == 'path':
                    pre_csv['source'].append(doc_inst['path'])
                elif key == 'y':
                    pre_csv['date'].append(doc_inst['y'])
                elif key in pre_csv.keys():
                    pre_csv[key] = pre_csv[key] + [''] * (len(pre_csv['group_id']) - len(pre_csv[key])) + [doc_inst[key]]
                else:
                    pre_csv = [''] * len(pre_csv['group_id']) + [doc_inst[key]]
            if 'text' not in doc_inst.keys():
                pre_csv['text'].append('')
            if 'path' not in doc_inst.keys():
                pre_csv['source'].append('')
            if 'y' not in doc_inst.keys():
                pre_csv['date'].append('')
            pre_csv['group_id'].append(doc['uid'])
    for key in pre_csv.keys():
        if len(pre_csv[key]) != len(pre_csv['group_id']):
            pre_csv[key] = pre_csv[key] + [''] * (len(pre_csv['group_id']) - len(pre_csv[key]))
    df = pd.DataFrame(pre_csv)
    df.to_csv("sample_csv.csv", index=False)
    return df

class ArgsSchema(Schema):
    topic = fields.Str()
    sources = fields.List(fields.Str())
    subtopics = fields.List(fields.Str())
    start_time = fields.DateTime()
    end_time = fields.DateTime()


# look into adding api call just with topic?
# use topic to display list of sources
# then run call similar to this with collection name and display source options
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
        # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
        client = MongoClient('mongodb+srv://umd3313:cornell@cluster0-e8xg6.mongodb.net/test?retryWrites=true&w=majority', tlsCAFile=certifi.where())
        database = client['AletheiaDataDesk']
        # Ukraine Russia
        topic_str = args['topic'] + " Inst"
        x = database.get_collection(topic_str)
        # example source list ["OJBBC", "OJFOX"]
        myquery = {
            'src': {'$in': args['sources']},
            'subt': {'$in': args['subtopics']},
            'end': {
                '$lt': args['end_time'],
                '$gt': args['start_time']
            }
        }
        cursor = x.find(myquery)
        df = doclist_to_output(cursor)
        print(df)
        # for document in cursor:
        #     print(document)
        #
        return MessageSchema().load({'message': 'testing api endpoint'})
