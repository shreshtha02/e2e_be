from pymongo import MongoClient

def get_db_handle():
    client = MongoClient(
        "mongodb+srv://test:12345@cluster0.3hdcb.mongodb.net/e2e_db?retryWrites=true&w=majority",authSource='admin')
    db = client.test
    db_handle = client['e2e_db']
    db_col = db_handle['personal_users']
    return db_col


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]