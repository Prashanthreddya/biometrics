from pymongo import MongoClient

def get_name_from_id(id):
    client = MongoClient()
    db = client.biometrics
    collection = db.users

    result = collection.find_one({'class': id})
    return result['name']
