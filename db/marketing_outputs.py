from .mongo import db
from datetime import datetime
import uuid
from typing import Optional, Dict, Any
collection = db['marketing_outputs']

def save_generated_posts(user_id: str, project_id: str, platforms: list[str], status: str, content: Optional[Dict[str,Any]] = None):
    # generated posts
    doc = {
        "user_id": user_id,
        "project_id": project_id,
        "batch_id": str(uuid.uuid4()), # generating unique batch id
        "platforms_used": platforms,
        "created_at": datetime.utcnow(),
        "last_updated": datetime.utcnow(),
        "status": status,
    }

    if content:
        doc["generated_content"] = content

    # inserting 
    collection.insert_one (doc)
    return doc ['batch_id']

def update_generated_posts(    
    batch_id: str,
    status: str,
    content: Optional[Dict[str,Any]] = None
    ) -> bool:
    update_fields = {
    "status": status,
    "last_updated": datetime.utcnow(),
    }

    if content:
        update_fields["generated_content"] = content
    
    result = collection.update_one(
        {"batch_id": batch_id},
        {"$set": update_fields}
    )
    # Return True if a document was modified
    return result.modified_count == 1

def get_post_batch_by_id(batch_id: str):
    return(collection.find_one(
        {"batch_id": batch_id},
        {"_id": 0}
    ))

def get_generated_posts(user_id: str , limit: int = 20):
    #fetching and sorting by latest and limiting number of posts
    return list(collection.find_one( #Using list to conver from cursor which is like a pointer to the result.
        {"user_id": user_id},
        {"_id": 0}
        ).sort("created_at", -1).limit(limit)) #sorting based on created at in descending and limit only reads sends upto the limit