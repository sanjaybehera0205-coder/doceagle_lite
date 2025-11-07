import uuid
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://sanjaybehera0205_db_user:JnvoPd57VXMhTGiO@firstproject.0yagecc.mongodb.net/?appName=firstproject"

client = AsyncIOMotorClient(MONGO_DETAILS, maxPoolSize=100)
database = client["firstproject"]
collection = database["user"]

# Create indexes once
async def create_indexes():
    await collection.create_index("user_id", unique=True)
    await collection.create_index("email", unique=True)

def serialize_user(user: dict) -> dict:
    if not user:
        return None
    user.pop("_id", None)  # remove MongoDB internal ID
    return user

projection = {"_id": 0, "user_id": 1, "name": 1, "email": 1, "age": 1}

async def create_user_db(user_data: dict) -> dict:
    user_data["user_id"] = str(uuid.uuid4())
    await collection.insert_one(user_data)
    user = await collection.find_one({"user_id": user_data["user_id"]}, projection)
    return serialize_user(user)

async def get_user_db(user_id: str) -> dict:
    user = await collection.find_one({"user_id": user_id}, projection)
    return serialize_user(user)

async def update_user_db(user_id: str, update_data: dict) -> dict:
    await collection.update_one({"user_id": user_id}, {"$set": update_data})
    updated_user = await collection.find_one({"user_id": user_id}, projection)
    return serialize_user(updated_user)
