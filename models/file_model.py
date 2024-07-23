from bson import ObjectId

def transform_object_id(data):
    if isinstance(data, list):
        return [transform_object_id(item) for item in data]
    elif isinstance(data, dict):
        return {key: transform_object_id(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    return data
 