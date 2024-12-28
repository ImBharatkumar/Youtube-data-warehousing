# import libraries
from sqlalchemy import create_engine, text
import pymongo, json

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



def connect_mysql():
    engine = create_engine('mysql+mysqlconnector://root:Bharatkori#1998@:3306/channel_data')
    with engine.connect() as conn:
        result = conn.execute(text("SHOW TABLES;"))
        for row in result:
            x = row[0]
            print(x)  # Optionally print or process the table name
        engine.dispose()
