from fastapi import FastAPI

from .crud import create_todo, delete_todo, fetch_all_todos_by_user, update_todo
from .models import NewTodo, Todo

app = FastAPI()


@app.post("/create")
async def read_root(todo: NewTodo):
    await create_todo(todo)
    return todo


@app.get("/todos_by_user")
async def get_all_todos(user: str):
    todos = await fetch_all_todos_by_user(user)
    return todos


@app.put("/update_todo/{id}")
async def update(id: str):
    item = await update_todo(id)
    return Todo(**item)


@app.delete("/delete_todo/{id}")
async def delete(id: str):
    item = await delete_todo(id=id)
    return Todo(**item)
