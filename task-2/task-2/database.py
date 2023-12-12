from pymongo import MongoClient

class Database:
    def __init__(self, db_url='mongodb://localhost:27017/', db_name='stock_data'):
        try:
            self.client = MongoClient(db_url)
            self.db = self.client[db_name]
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def insert_data(self, collection_name, data):
        try:
            collection = self.db[collection_name]
            collection.insert_one(data)
            print(f"Data inserted into {collection_name} collection")
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")
