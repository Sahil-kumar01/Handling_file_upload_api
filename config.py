import os

UPLOAD_DIR = 'static/uploads/'
CONVERTED_DIR = 'static/converted/'
mongo_url = 'mongodb+srv://sahilkumarktp16:S%40hil2003@mongoy.q4auz7c.mongodb.net/files'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)
