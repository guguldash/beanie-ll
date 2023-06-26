from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from student2.std import STD
from dotenv import load_dotenv
import os


load_dotenv()

async def init():
    client  = AsyncIOMotorClient(os.getenv("CONNECTION_STRING"))
    await init_beanie(database=client.sample_db_1, document_models=[STD])
    
    
    
    

