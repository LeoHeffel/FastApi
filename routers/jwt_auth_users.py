from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 180
SECRET= "0cd011703be118b57b91f8ae7da004826bc007a73a2519c31ee624f15b1306e8"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class User_DB(User):
    hashed_password: str


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "Hk0pG@example.com",
        "disabled": False,
        "hashed_password": "$2a$12$vMUyniT.wTD1h0fELWhkge.Akr6Z7cZrNPuN2gpNBCscVglGXZFsC",
    },
    "janedoe": {
        "username": "janedoe",
        "full_name": "Jane Doe",
        "email": "UZQpK@example.com",
        "disabled": True,
        "hashed_password": "$2a$12$vMUyniT.wTD1h0fELWhkge.Akr6Z7cZrNPuN2gpNBCscVglGXZFsC",
    },
    "admin": {
        "username": "admin",
        "full_name": "Admin",
        "email": "Hk0pG@example.com",
        "disabled": False,
        "hashed_password": "$2a$12$vMUyniT.wTD1h0fELWhkge.Akr6Z7cZrNPuN2gpNBCscVglGXZFsC",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return User_DB(**users_db[username])
    
def search_user(username: str):
    print(username,"isername")
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token:str = Depends(oauth2)):

    exeption = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    try:
        username=jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeption
    except JWTError:
        raise exeption
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}



@router.get("/me")
async def me(user: User = Depends(current_user)):
    return user