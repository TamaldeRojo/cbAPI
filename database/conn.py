import motor.motor_asyncio
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_URI = os.getenv('MONGO_URL')


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.chatbox
