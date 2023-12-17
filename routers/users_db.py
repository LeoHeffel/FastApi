from fastapi import APIRouter, HTTPException
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(prefix="/usersdb",tags=["usersdb"] ,responses={404: {"description": "Not found"}})








@router.get("/",response_model=list[User] )
async def get_users():
    users = db_client.local.users.find()
    return  users_schema(users)
     


@router.get("/{user_id}")
async def get_user_by_id(user_id: str):
    if  not ObjectId.is_valid(user_id):
        raise  HTTPException(status_code=400, detail="Invalid Id")
    else:
        return search_user("_id",ObjectId(user_id))



@router.post("/",response_model=User, status_code=201)
async def create_user(user: User):
    
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status_code=400, detail="User already exists")
    user_dict = dict(user)
    del user_dict["id"]
    try:
        id = db_client.local.users.insert_one(user_dict).inserted_id
        new_user = user_schema(db_client.local.users.find_one({"_id": id}))
    except:
        raise HTTPException(status_code=400, detail="Error creating user")

    return User(**new_user)


@router.put("/",response_model=User)
async def update_user(user: User):
    if  not ObjectId.is_valid(user.id):
        raise  HTTPException(status_code=400, detail="Invalid Id")
    else:
        try:
            user_dict = dict(user)
            del user_dict["id"]
            update_user= db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
            if not update_user:
                return  HTTPException(status_code=404, detail="User not found") 
        except:
            return {"error": "User not modified"}
    return search_user("_id",ObjectId(user.id))


@router.delete("/{user_id}" ,status_code=204)
async def delete_user(user_id: str):
    if  not ObjectId.is_valid(user_id):
        raise  HTTPException(status_code=400, detail="Invalid Id")
    else:
        found = db_client.local.users.find_one_and_delete({"_id": ObjectId(user_id)})
        if not found:
            return {"error": "User not found"}
        return 


def search_user(field:str, value):
    try:
       user = db_client.local.users.find_one({field: value})
       return User(**user_schema(user))
    except:
        return {"error": "User not found"}
  