from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",tags=["users"] ,responses={404: {"description": "Not found"}})


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    email: str


users_list = [
    User(id=1, name="user1", surname="surname1", age=1, email="email1"),
    User(id=2, name="user2", surname="surname2", age=2, email="email2"),
    User(id=3, name="user3", surname="surname3", age=3, email="email3"),
]


@router.get("/usersjson")
async def get_users_json():
    return {"users": ["user1", "user2"]}


@router.get("/")
async def get_users():
    return users_list


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    return search_user(user_id)


@router.get("/userquery/")
async def get_user_by_id(user_id: int):
    return search_user(user_id)


@router.post("/", status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
       raise HTTPException(status_code=400, detail="User already exists")
    users_list.append(user)
    return user


@router.put("/")
async def update_user(user: User):
    found = False

    for i, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[i] = user
            found = True
    if not found:
        return {"error": "User not found"}

    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    found = False
    for i, saved_user in enumerate(users_list):
        if saved_user.id == user_id:
            users_list.pop(i)
            found = True
    if not found:
        return {"error": "User not found"}
    return 


def search_user(user_id):
    user = filter(lambda user: user.id == user_id, users_list)
    try:
        return list(user)[0]
    except:
        return {"error": "User not found"}
