from fastapi import FastAPI
from routes import file_routes

app = FastAPI()

app.include_router(file_routes.router)

