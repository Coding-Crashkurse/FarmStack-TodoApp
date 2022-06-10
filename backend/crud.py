from bson.errors import InvalidId
from bson.objectid import ObjectId
from fastapi import HTTPException

from .db import collection
from .models import Todo


async def delete_todo(todo):
    document = dict(todo)
    await collection.insert_one(document)


async def create_todo(todo):
    document = dict(todo)
    await collection.insert_one(document)


async def update_todo(id):
    try:
        document = await collection.find_one({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id not correct")
    if not document:
        raise HTTPException(status_code=404, detail="Item not found")
    new_val = not document["done"]
    updated_todo = await collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": {"done": new_val}}
    )
    return updated_todo


async def delete_todo(id):
    try:
        item = await collection.find_one_and_delete({"_id": ObjectId(id)})
    except InvalidId:
        raise HTTPException(status_code=422, detail="Id not correct")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


async def fetch_all_todos_by_user(user):
    todos = []
    cursor = collection.find({"user": {"$eq": user}})
    async for document in cursor:
        print(document)
        print(document["_id"])
        todo = Todo(**document)
        todos.append(todo)
    return todos
