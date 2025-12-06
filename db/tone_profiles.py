from .mongo import db
from datetime import datetime

collection = db['tone_profiles']

def save_tone_profile(user_id: str, tone_data: dict):
    # tone profile for user
    doc = {
        # "user_id": user_id,
        # "tone": tone_data,
        **tone_data,
        "updated_at": datetime.utcnow()
    }
    #inserting tone profile or updating if exists using upsert
    collection.update_one (
        {"user_id": user_id},
        {"$set": doc},
        upsert = True
    )
    return
def get_tone_profile(user_id: str):
    #fetching tone proile for user
    return collection.find_one({"user_id": user_id}, {"_id":0})