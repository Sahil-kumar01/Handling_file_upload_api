import os

UPLOAD_DIR = 'static/uploads/'
CONVERTED_DIR = 'static/converted/'
mongo_url = 'mongodb://localhost:27017/'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)
