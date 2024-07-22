from fastapi import APIRouter, UploadFile, File, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from utils.file_utils import convert_to_pdf, is_pdf
from models.file_model import transform_object_id
import datetime
import aiofiles
import os
from config import UPLOAD_DIR, CONVERTED_DIR,mongo_url

router = APIRouter()

client = AsyncIOMotorClient(mongo_url)
db = client.filedb

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    verification_start = datetime.datetime.now()
    verification_end = None
    converted = False
    conversion_start = None
    conversion_end = None
    converted_file_path = None

    if not is_pdf(filename):
        conversion_start = datetime.datetime.now()
        converted_file_name = f"{os.path.splitext(filename)[0]}.pdf"
        converted_file_path = os.path.join(CONVERTED_DIR, converted_file_name)
        convert_to_pdf(file_path, converted_file_path)
        conversion_end = datetime.datetime.now()
        converted = True

    verification_end = datetime.datetime.now()

    await db.files.insert_one({
        "name": filename,
        "location": file_path,
        "verification_start": verification_start,
        "verification_end": verification_end,
        "converted": converted,
        "conversion_start": conversion_start,
        "conversion_end": conversion_end,
        "converted_location": converted_file_path
    })

    return {
        "name": filename,
        "original_location": file_path,
        "converted": converted,
        "converted_location": converted_file_path
    }

@router.get("/files/")
async def list_files(converted: bool = None, hours: int = None):
    query = {}
    if converted is not None:
        query["converted"] = converted
    if hours is not None:
        time_threshold = datetime.datetime.now() - datetime.timedelta(hours=hours)
        query["verification_end"] = {"$gte": time_threshold}

    files = await db.files.find(query).to_list(None)
    return transform_object_id(files)

@router.get("/files/converted/")
async def list_converted_files():
    files = await db.files.find({"converted": True}).to_list(None)
    return transform_object_id(files)

@router.get("/files/non-converted/")
async def list_non_converted_files():
    files = await db.files.find({"converted": False}).to_list(None)
    return transform_object_id(files)

@router.get("/files/last-24-hours/")
async def list_files_last_24_hours():
    time_threshold = datetime.datetime.now() - datetime.timedelta(hours=24)
    files = await db.files.find({"verification_end": {"$gte": time_threshold}}).to_list(None)
    return transform_object_id(files)

@router.get("/files/last-48-hours/")
async def list_files_last_48_hours():
    time_threshold = datetime.datetime.now() - datetime.timedelta(hours=48)
    files = await db.files.find({"verification_end": {"$gte": time_threshold}}).to_list(None)
    return transform_object_id(files)

@router.get("/download/{file_name}")
async def download_file(file_name: str, destination: str):
    file_doc = await db.files.find_one({"converted_location": os.path.join(CONVERTED_DIR, file_name)})
    if not file_doc:
        raise HTTPException(status_code=404, detail="File not found")

    source_path = file_doc["converted_location"]
    if not os.path.exists(source_path):
        raise HTTPException(status_code=404, detail="Converted file not found")

    os.makedirs(destination, exist_ok=True)
    destination_path = os.path.join(destination, file_name)
    os.rename(source_path, destination_path)

    return {"message": f"File copied to {destination_path}"}
