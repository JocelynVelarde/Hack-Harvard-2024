from mongo_connection import insert_json_file

def main():
    # Define the path to your JSON file
    json_file_path = 'assets/data.json'
    
    # Define the database and collection names
    database_name = 'json'
    collection_name = 'json_live_video'
    
    try:
        # Call the insert_json_file method to upload the JSON data
        insert_json_file(json_file_path, database_name, collection_name)
        print("JSON file uploaded successfully.")
    except Exception as e:
        print(f"Failed to upload JSON file: {e}")

if __name__ == '__main__':
    main()