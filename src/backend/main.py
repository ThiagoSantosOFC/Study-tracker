from dotenv import load_dotenv
import os
from fastapi import FastAPI

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

# Create FastAPI instance with a route prefix
app = FastAPI()

@app.get("/api/v1/")
def read_root():
    return {"Hello": "World"}

# Additional routes can be added here
@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}