from .mongo import db
from datetime import datetime
from bson.objectid import ObjectId
import uuid
from typing import Optional, Any, Dict

collection = db["business_profiles"]

def create_new_project(user_id: str, profile_data: dict):
    project_id = str(uuid.uuid4())
    doc = {
        "project_id": project_id,
        "user_id": user_id,
        **profile_data,
        "ai_strategy_status": "PENDING", # Initial status
        "ai_suggested_strategy": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    # insert the new document
    collection.insert_one(doc)
    
    # return the new UUID
    return project_id

def save_business_profile(user_id: str, project_id: str, update_data: Dict[str, Any]) -> bool:
    update_data["update_at"] = datetime.utcnow()

    # inserting or updating business profile
    result = collection.update_one(
        {"project_id": project_id, 'user_id': user_id},
        {"$set": update_data},
    )
    return result.modified_count == 1 # Return True if a document was modified

def get_business_profile(user_id:str, project_id: str):
    #fetching biz profile
    return collection.find_one({"user_id": user_id, "project_id": project_id}, {"_id":0})
     

def update_project_strategy_success(
    project_id: str,
    status: str,
    strategy_data: Optional[Dict[str,Any]] = None
    ) -> bool:
    update_fields = {
    "ai_strategy_status": status,
    "last_updated": datetime.utcnow(),
    }

    if strategy_data:
        update_fields["ai_suggested_strategy"] = strategy_data
    
    result = collection.update_one(
        {"project_id": project_id},
        {"$set": update_fields}
    )
    # Return True if a document was modified
    return result.modified_count == 1 

