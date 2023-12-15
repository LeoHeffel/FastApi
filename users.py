from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    email: str

users_list = [
    User(id=1, name="user1", surname="surname1", age=1, email="email1"),
    User(id=2, name="user2", surname="surname2", age=2, email="email2"),
    User(id=3 , name="user3", surname="surname3", age=3, email="email3"),
]

@app.get("/usersjson")
async def get_users_json():
    return {"users": ["user1", "user2"]}


@app.get("/users")
async def get_users():
    return users_list

@app.get("/user/{user_id}")
async def get_user_by_id(user_id: int):
   user = filter(lambda user: user.id == user_id, users_list)
   try :
       return list(user)[0]
   except:
       return {"error": "User not found"}
   
@app.get("/userquery/")
async def get_user_by_id( user_id: int  ):
   
   user = filter(lambda user: user.id == user_id, users_list)
   try :
       return list(user)[0]
   except:
       return {"error": "User not found"}