import pymongo
from pymongoarrow.api import Schema
from utils.configuration import Configuration
from pymongo import MongoClient


client = MongoClient(Configuration.load('database_connections:mongodb:default'))

conversation_db = client.get_database('conversation_db')

message_chunk_collection = conversation_db.create_collection('message_chunk')
message_collection = conversation_db.create_collection('message')


message_chunk_collection.insert_many([
    {
        'conversation_id': '',
        'created_at': '',
        'no_of_chunk': '',
        'limit_length': 20,
        'length': 1,
        'id': ''
    }
])

message_collection.insert_many([
    {
        'conversation_id': '',
        'chunk_id': '',
        'attendee_id': '',
        'reference_msg_id':'',
        'content': '',
        'created_at': '',
        'updated_at': '',
        'feedback': '',
        'state': '',
        'no_of_msg': 1,
        'document': [],
        'id': ''
    }
])

client.close()