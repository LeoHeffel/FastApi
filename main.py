from fastapi import FastAPI
from routers import products, users



app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}   

@app.get("/url")
async def url():
    return {"url": "http://127.0.0.1:8000"}
