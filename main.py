import os
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import mysql.connector
import pymongo
import json
from PIL import Image
from src.channel_data import get_channel_data
from src.database import export_to_mongodb
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

if __name__ == "__main__":
    get_channel_data("UCIsz3XD8_E1ebhE4YScWeJg", api_key)
    export_to_mongodb("data/channel_data.json")





