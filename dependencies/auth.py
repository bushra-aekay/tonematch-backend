# dependencies/auth
# 8. get current user reads the cookie, calls the service to decofe and validate the session jwt (signature, expiry, type)
# 9. uses the verified sub(user id) to fetch the full user object from db and passes it tot route handler

from fastapi import Request, HTTPException, status, Depends
from services.auth import decode_and_validate_token
from db.users import get_user_by_id
from typing import Dict, Any

SESSION_COOKIE_NAME = "session_token"

# fn that requires object to read the cookie
async def get_current_user(request: Request) -> Dict[str, Any]:
    # Reads the session JWT from the HTTP-only cookie, validates it, and returns the user object.
    
    # Get the JWT from HTTP-only cookie
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        # No cookie/token, user is aunauthorized
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Session token missing.",
            # headers={"WWW-Authnticate": "Bearer"},
        )
    try: 
        # Decode and Validate the token (signature, expiry, etc.)
        payload = decode_and_validate_token(token)
    # 3. Security Check: Must be a long-lived session token
        if payload.get("type") != "session":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type.")
        user_id = payload.get("sub")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme.")
    
    user = get_user_by_id(user_id)
    if not user or not user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user account inactive or not found")
    return user


# a helper to get the ID
def extract_user_id(user_data: Dict[str, Any] = Depends(get_current_user)) -> str:
    user_id = user_data.get('user_id')
    print(user_id)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User ID not found.")
    return user_id