# auth/service.py - decoding and validating any token
# 5. If validated is token of clicked link, create a long-lived session jwt containing users id (sub) and type as session
from jose import JWTError, jwt
from fastapi import HTTPException, status
from typing import Dict, Any
from utils.auth import SECRET_KEY, ALGORITHM, create_session_jwt
from db.users import get_user_by_id

# verification and decode fn
def decode_and_validate_token(token: str) -> Dict[str, Any]:
    # decodes, validates the token signature and expiry, and returns the payload
    try:
        # decode the token - checks signature and expiry, returns the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #decoding the token
        if payload.get("sub") is None:
            raise JWTError("Token missing id")
        return payload # return decoded data if exists
    except jwt.ExpiredSignatureError:
        # specifc - expired token - err
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="expired token")
    except JWTError:
        # general error 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavlid token")

def verify_link_and_get_session(token: str) -> str:
    # Validates the magic link token.
    # 2. Issues and returns a long-lived 'session' JWT.
    payload = decode_and_validate_token(token)
    if payload.get("type") != "link":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    user_id = payload.get("sub")
    user = get_user_by_id(user_id)
    if not user or not user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account inactive or not found")
    session_jwt = create_session_jwt(user_id=user_id)
    return session_jwt


# def get_current_user_from_session(token: str) -> dict:
#     # """Decodes the session JWT and fetches the full user record."""
#     payload = decode_and_validate_token(token)
#     # Ensure it's a session token (to prevent using a magic link token here)
#     if payload.get("type") != "session":
#         raise HTTPException(status_code=401, detail="token aint a sess token")
#     user = get_user_by_id(payload.get("user_id"))

#     if user is None: 
#         raise HTTPException(status_code=401, detail="User not found")
#     return user



