import os
import pymongo


connection = {}


def _get_connection():
    global connection
    # get the process if
    pid = os.getpid()

    # if there is a connection based on the current id use it otherwise create a new one
    if connection and connection.get(pid):
        return connection[pid]

    else:
        connection[pid] = pymongo.MongoClient('mongodb+srv://40179863:Deano8505DOD9997@search-engine-40179863-0hak5.gcp.mongodb.net/test?retryWrites=true&w=majority')

    return connection[pid]


def connect_to_db(collection=None):
    conn = _get_connection()
    conn = conn['search_engine']

    # this is for if there is multiple collections you can specify which one
    if collection:
        return conn[collection]
    # do original setup to create used collection
    if 'list_of_words' not in conn.collection_names():
        conn.create_collection('list_of_words',
                                 collation={"locale": "en", "strength": 1})
    return conn


