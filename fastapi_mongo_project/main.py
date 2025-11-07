from fastapi import FastAPI, HTTPException
from models import UserCreate
from src.shared.database.db import create_user_db, get_user_db, update_user_db

app = FastAPI()


@app.post("/users/")
async def create_user(user: UserCreate):
    created_user = await create_user_db(user.dict())
    return created_user


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await get_user_db(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}")
async def update_user(user_id: str, user: UserCreate):
    updated_user = await update_user_db(user_id, user.dict())
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")
