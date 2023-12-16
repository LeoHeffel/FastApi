from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "hashed_password": "fakehashedsecret",
    },
    "janedoe": {
        "username": "janedoe",
        "full_name": "Jane Doe",
        "email": "UZQpK@example.com",
        "disabled": True,
        "hashed_password": "fakehashedsecret2",
    },
    "admin": {
        "username": "admin",
        "full_name": "Admin",
        "email": "Hk0pG@example.com",
        "disabled": False,
        "hashed_password": "fakehashedsecret3",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return User_DB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )
    user = search_user_db(form.username)
    if form.password != user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
