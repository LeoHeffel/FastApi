from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
URI = os.environ.get("MONGO_URI")
db_client = MongoClient( URI ).FastApi