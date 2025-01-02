
from datetime import datetime
from sqlalchemy import create_engine
import pymongo, json

# Define utility functions
def convert_iso_to_mysql_datetime(iso_date_str):
    dt = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# Define utility functions
def convert_duration_to_seconds(duration):
    import isodate
    return int(isodate.parse_duration(duration).total_seconds())


# Establish connection to the MySQL database
def connect_mysql():
    engine = create_engine('mysql+mysqlconnector://root:Bharatkori#1998@localhost:3306/channel_data')
    return engine


# Export data to MongoDB
def export_to_mongodb(channel_data: json):
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["Youtube_data"]
        collection = db["channel_dataset"]

        # Load data from JSON file
        with open(channel_data, 'r') as file:
            data = json.load(file)

        # insert data into MangoDB
        if data:
            # Insert the channel data into MongoDB
            collection.insert_one(data)
            print("Data inserted into MongoDB.")
            db.close()
        else:
            print("Error retrieving channel data.")
            

# fetch_channel_data_from_mongodb
def fetch_channel_data_from_mongodb():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["Youtube_data"]
    collection = db["channel_dataset"]
    # Fetch data from MongoDB
    data = collection.find_one()
    return data