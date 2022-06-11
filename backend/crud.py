from bson.errors import InvalidId
from bson.objectid import ObjectId
from fastapi import HTTPException

from .db import collection, user_collection
from .models import Todo

# Add User


async def create_user(user):
    user = dict(user)
    document = await user_collection.find_one({"username": user["username"]})
    if document:
        raise HTTPException(status_code=409, detail="User already registered")
    await user_collection.insert_one(user)


# Add Todos


async def create_todo(todo, user):
    document = dict(todo, **{"username": user["username"]})
    print(document)
    await collection.insert_one(document)


async def update_todo(id, user):
    try:
        document = await collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id not correct")
    if not document:
        raise HTTPException(status_code=404, detail="Item not found")
    if user["username"] != document["username"]:
        raise HTTPException(status_code=403, detail="Not allowed to update item")
    new_val = not document["done"]
    updated_todo = await collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"done": new_val}}
    )
    return updated_todo


async def delete_todo(id, user):
    try:
        document = await collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id not correct")
    if not document:
        raise HTTPException(status_code=404, detail="Item not found")
    if user["username"] != document["username"]:
        raise HTTPException(status_code=403, detail="Not allowed to update item")
    document = await collection.find_one_and_delete({"_id": ObjectId(id)})
    return document


async def fetch_all_todos_by_user(user):
    todos = []
    cursor = collection.find({"username": {"$eq": user["username"]}})
    async for document in cursor:
        print(document["_id"])
        todo = Todo(**document)
        todos.append(todo)
    return todos
