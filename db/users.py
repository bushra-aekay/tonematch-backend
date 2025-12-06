from .mongo import db
from datetime import datetime
import uuid
from pymongo.errors import PyMongoError
from fastapi import HTTPException, status
from typing import Optional, Dict, Any

user_collection = db['users']

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    # fetches user record by email and excluding mongos _id field
    try: 
        return user_collection.find_one({"email": email}, {"_id": 0})
    except PyMongoError as e:
        # catching any mongo access error
        print(f"Database err: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="db errr"
        )
    

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    # fetches user record by the unique 'user_id'
    try:
        return user_collection.find_one({"user_id": user_id}, {"_id": 0})
    except PyMongoError as e:
        # catching any mongo access error
        print(f"Database err: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="db errr"
        )
    

def get_or_create_user(email: str)-> Dict[str, Any]:
    # retrieves an existing user or creates a new one if not found.
    # check for existing user
    try: 
        user = get_user_by_email(email)
        if user:
            return user
    except HTTPException:
        raise
        # user doesn't exist, so create the record
    new_user = {
        "user_id": str(uuid.uuid4()),
        "email": email,
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    # insert into MongoDB
    try:
        user_collection.insert_one(new_user)
        return get_user_by_email(email) 
    except PyMongoError as e:
        # catching any mongo access error
        print(f"Database err for user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to create user rec due to err"
        )
    
   

