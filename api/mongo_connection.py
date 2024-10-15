
from pymongo.server_api import ServerApi
from pymongo import MongoClient
import streamlit as st
import gridfs
import json
from bson import ObjectId
from datetime import datetime

client = MongoClient(st.secrets["MONGO"]["MONGO_URI"], tls=True, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()  # Converts datetime to ISO 8601 string
        return json.JSONEncoder.default(self, o)

def insert_data(data :str, database: str, collection: str) -> str:
    try:
        database =  client.get_database(database)
        collection = database.get_collection(collection)
        
        result = collection.insert_one(data)
        
        print(f'Data inserted successfully with id: {result.inserted_id}')
    except Exception as e:
        print("Error inserting data: ", e)

def insert_file(filepath: str, database: str) -> str:
    try:
        database = client.get_database(database)
        bucket = gridfs.GridFSBucket(database)

        with bucket.open_upload_stream(filepath) as upload_stream:
            upload_stream.write(open(filepath, "rb").read())
        
        print(f'Data inserted successfully')
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

def get_file(filename: str, database: str):
    try:
        database =  client.get_database(database)
        bucket = gridfs.GridFSBucket(database)

        with bucket.open_download_stream_by_name(filename=filename) as download_stream:
            data = download_stream.read()
            with open(filename, "wb") as f:
                f.write(data)
        
        print (f'Data retrieved successfully with id: {download_stream.filename}')
    except Exception as e:
        print("Error retrieving data: ", e)

def insert_json_file(filepath: str, database: str, collection: str) -> str:
    try:
        database = client.get_database(database)
        collection = database.get_collection(collection)

        with open(filepath, 'r') as file:
            data = json.load(file)
        
        # Wrap the data in a single parent object if it's a list
        if isinstance(data, list):
            data = {"data": data}

        # add filename property to the data
        data['filename'] = filepath

        result = collection.insert_one(data)
        print(f'Data inserted successfully with id: {result.inserted_id}')
    except Exception as e:
        print("Error inserting data: ", e)
