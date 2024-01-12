from src.exception import CustomException
from src.logger import logging
import sys
import os 
from pymongo import MongoClient


#  database 


class Database:
    client = None
    db = None
    def __init__(self,database_name, host='localhost', port=27017):
        self.database_name = database_name
        self.client = MongoClient(host=host, port=port,document_class=dict)
        self.db = self.client[database_name]


    # def connect_to_mongodb(self):
    #     # Connect to the MongoDB server
    #     self.client.connect()


    def insert_data(self, collection_name,data):

        collection = self.db[collection_name]
        result = collection.insert_one(data)

        # self.client['test_ml']['test_ml'].insert_one(data)

        return result.inserted_id


    def get_data(self, collection_name):
        """
        Get data from the specified collection.

        :param collection_name: Name of the collection to retrieve data from.
        :param query: (Optional) Query to filter data (dictionary).
        :return: List of documents that match the query.
        """


        collection = self.db[collection_name]

        # if query is None:
        result = collection.find()
        # else:
        #     result = collection.find(query)


        return list(result)
    
    # def get_data(self):
    #     # Retrieve all documents from the api_data collection
    #     return list(self.client['test_ml']['test_ml'].find())

    def close_connection(self):
        # Close the connection to the MongoDB server
        self.client.close()

        


'''
How to use the database connection in other files 

# # '''
# # Create an instance of the Database class
# db = Database(dat)

# # # Connect to the MongoDB server
# # db.connect_to_mongodb()


# # # Insert some data
# # data = {'name': 'Adnane Aboutalib', 'age': 22}
# inserted_id = db.insert_data(collection_name='test_ml',data=data)
# # print(f"Data inserted with ID: {inserted_id}")



# # # # Retrieve all documents from the api_data collection
# # data = db.get_data()
# # print(data)

# # # Close the connection to the MongoDB server
# # db.close_connection()


    