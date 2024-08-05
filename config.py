import os

UPLOAD_DIR = 'static/uploads/'
CONVERTED_DIR = 'static/converted/'
mongo_url = 'your_mongo_db_link'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)
