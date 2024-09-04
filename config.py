import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGODB_TOKEN = os.getenv('MONGODB_TOKEN')

ADMINS = [588093669, 956945958, 6252741731]

client = AsyncIOMotorClient(MONGODB_TOKEN)
db = client.replay