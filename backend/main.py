from fastapi import FastAPI
from fastapi_login import LoginManager
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.middleware.cors import CORSMiddleware

from .db import user_collection
from .crud import (
    create_todo,
    delete_todo,
    fetch_all_todos_by_user,
    update_todo,
    create_user,
)
from .models import NewTodo, Todo, User

SECRET = "super-secret-key"
manager = LoginManager(SECRET, "/login")


@manager.user_loader()
async def query_user(username):
    document = await user_collection.find_one({"username": username})
    return document


app = FastAPI(
    title="Fullstack Todo-App",
    description="Full stack todo App mit JWT Login (Authentication und Authorization)",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def new_user(user: User):
    await create_user(user)
    return user


@app.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = await query_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": username})
    return {"access_token": access_token}


@app.post("/create_todo")
async def new_todo(todo: NewTodo, user=Depends(manager)):
    await create_todo(todo, user)
    return todo


@app.get("/get_todos_by_user")
async def get_all_todos(user=Depends(manager)):
    todos = await fetch_all_todos_by_user(user)
    return todos


@app.put("/update_todo/{id}")
async def update(id: str, user=Depends(manager)):
    item = await update_todo(id, user)
    return Todo(**item)


@app.delete("/delete_todo/{id}")
async def delete(id: str, user=Depends(manager)):
    item = await delete_todo(id, user)
    return Todo(**item)
