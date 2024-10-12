
from pymongo.server_api import ServerApi
from pymongo import MongoClient
import streamlit as st

client = MongoClient(st.secrets["MONGO_URI"], tls=True, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))

import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def insert_data(data :str, database: str, collection: str) -> str:
    try:
        database =  client.get_database(database)
        collection = database.get_collection(collection)
        
        result = collection.insert_one(data)
        
        print(f'Data inserted successfully with id: {result.inserted_id}')
    except Exception as e:
        print("Error inserting data: ", e)

def get_one_data(query: str, database: str, collection: str) -> str:
    try:
        database =  client.get_database(database)
        collection = database.get_collection(collection)
        
        data = collection.find_one(query)
        
        return JSONEncoder().encode(data)
    
    except Exception as e:
        print("Error getting data: ", e)
        return {"error": f'Error getting data {e}'}

def get_all_data(database: str, collection: str) -> str:
    try:
        database =  client.get_database(database)
        collection = database.get_collection(collection)
        
        data = collection.find({})
        
        result = [] 
        for d in data:
            result.append(d)  
        
        return JSONEncoder().encode(result)
    except Exception as e:
        print("Error getting data: ", e)
        return {"error": f'Error getting data {e}'}


