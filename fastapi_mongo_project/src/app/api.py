from fastapi import FastAPI, HTTPException
from models import UserCreate
from src.shared.database.db import get_collection
from bson import ObjectId

app = FastAPI()
collection = get_collection()


@app.post("/users/")
async def create_user(user: UserCreate):
    user_dict = user.dict()
    result = await collection.insert_one(user_dict)
    created_user = await collection.find_one({"_id": result.inserted_id})
    created_user["_id"] = str(created_user["_id"])  # convert ObjectId to string
    return created_user


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")
