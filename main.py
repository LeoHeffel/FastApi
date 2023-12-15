from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}   

@app.get("/url")
async def url():
    return {"url": "http://127.0.0.1:8000"}
