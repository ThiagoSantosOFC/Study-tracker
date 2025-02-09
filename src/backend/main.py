from dotenv import load_dotenv
import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
