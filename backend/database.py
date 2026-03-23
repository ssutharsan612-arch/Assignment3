import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["yourfullname_network_incidents_db"]
users = db["users"]
incidents = db["incidents"]