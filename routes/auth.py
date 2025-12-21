# routes/auth.py --
# 1. handling when users enters the email and submits the form
# 3. sending unique link via email to user
# 4. Once the user clicks the link validate the token w sign and expiry and check type is magic link
# 6. Set the session JWT in a HTTP-only cookie in the HTTP response header and redirect user to page
# 7. User requests protect route then browser auto attaches HTTP-only cookie containing session JWT to the cookie
from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse
from db.users import get_or_create_user
from models.auth import EmailRequest
from utils.auth import create_link_token
from services.auth import verify_link_and_get_session
from jose import JWTError
from dependencies.auth import get_current_user
import os
from services.email_service import send_link_to_email
# from typing import Dict, Any

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")
SESSION_COOKIE_NAME = "session_token"

router = APIRouter(prefix="/auth", tags=["Auth"]) 

# request link endpoint
@router.post('/request-link', status_code=status.HTTP_200_OK) ## Frontend -- used in LoginForm.tsx
async def request_magic_link(request: EmailRequest):
    # receives email, creates/retrieves user, creates Magic Link token, and (for now) simulates sending email.
    user = get_or_create_user(request.email)
    link_token = create_link_token(user_id = user["user_id"])
    url = f"{FRONTEND_BASE_URL}/verify-login?token={link_token}"

    # integrate real email client here
    send_link_to_email(recipent_email=request.email, url=url)
    # local testing
    print("-" * 50)
    print(f"DEBUG: Link for {request.email}: {url}")
    print("-" * 50)
    
    return {"message": "Magic link sent successfully. Please check your email."}

# verifying link and issuing session jwt
@router.get("/verify")
async def verify_link_endpoint(token: str, response: Response):
    # Verifies the magic link token via the service layer and sets the secure, HTTP-only cookie. 
    try:
        session_jwt = verify_link_and_get_session(token)
    except HTTPException as e:
        raise e 
        
    #  setting the HTTP-only cookie
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_jwt,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 7 # 7 days 
    )

    return {"message": "login success. sess started" }

 
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {"message": "Log out success"}

# testing/checking whether user was created
@router.get('/me', status_code=status.HTTP_200_OK)
async def read_user_me(
    current_user: dict = Depends(get_current_user)
):
    return current_user
