# auth/utils.py - fjs for creating JWTs
# 2. creates a short lived jwt when the user is new 
# also creates the long-lived session token.
import os # for env variables
from datetime import datetime, timedelta 
from jose import jwt
from typing import Dict, Optional, Any 

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key") # to sign the JWT and if not found, use dev-key
ALGORITHM = "HS256" # symmetric signing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # session tokens that expire in 7 days
LINK_EXPIRE_MINUTES = 10 # link tokens that expire in 10 mins

# link token Generator - a shortlived, link type jwt, when the user is new 
def create_link_token(user_id:str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=LINK_EXPIRE_MINUTES)
    to_encode: Dict[str, Any] = {
        "sub": user_id,
        "exp": expire,
        "type": "link"
    }
    # sign (encode) the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# creating session token fn - a long lived jwt for session after verification success
def create_session_jwt(user_id:str, expires_delta: Optional[timedelta] = None) -> str: # data contains id and email, expires delta is for custom expiry time and timedelta is a duration 
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) # expiry time is current time plus expires_delta(Custom, if provided) or default
    to_encode: Dict[str, Any] = {
        "sub": user_id,
        "exp": expire,
        "type": "session"
    }
    # sign (encode) the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # encoding the data w secret key and algo
    return encoded_jwt # returns signed jwt string
