from bson.objectid import ObjectId as BsonObjectId
from pydantic import BaseModel, Field


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError("ObjectId required")
        return str(v)


class NewTodo(BaseModel):
    user: str
    description: str
    done: bool = False


class Todo(NewTodo):
    id: PydanticObjectId = Field(..., alias="_id")


class User(BaseModel):
    username: str
    password: str