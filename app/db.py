from flask_pymongo import PyMongo
mongo = PyMongo() 

class mongoQuery():

    def save(data,colletion):
        id=mongo.db[colletion].insert_one(data)
        return  str(id)
    def delete(data,colletion):
        id=mongo.db[colletion].delete_one(data)
        return  str(id)
    def get(data,colletion):
        id=mongo.db[colletion].find_one(data)
        return  id