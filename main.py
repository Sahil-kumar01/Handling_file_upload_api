from fastapi import FastAPI
from routes import file_routes

app = FastAPI()

app.include_router(file_routes.router)

git add main.py
git add routes/file_routes.py