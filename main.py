import os
from src.channel_data import get_channel_data
from src.utility import export_to_mongodb
from srr.database import write_to_sql
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variable
api_key = os.getenv('YOUTUBE_API_KEY')

# Check if the API key was successfully retrieved
if api_key:
    print("API Key:", api_key)
else:
    print("Error: YOUTUBE_API_KEY environment variable not set.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/sushidolly/.config/gcloud/application_default_credentials.json"

if __name__=="__main__":
    get_channel_data("UCIsz3XD8_E1ebhE4YScWeJg", api_key)
    export_to_mongodb("data/channel_data.json")
    write_to_sql()



