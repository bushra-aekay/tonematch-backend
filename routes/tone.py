#routes/tone.py
from fastapi import APIRouter, Depends
from typing import Dict, Any
from services.tone import analyze_tone
from db.tone_profiles import get_tone_profile
from models.tone import ToneRequest
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/tone", 
    tags=['Tone']
)

@router.post("/analyze-tone") #api endpoint
def analyze_tone_result(request: ToneRequest, user_data: Dict[str, Any] = Depends(get_current_user)): #function and request is the name/reference of the incoming data
    user_id = user_data.get('user_id')
    result = analyze_tone(request.posts, user_id)
    return result

@router.get("/get-tone-profile/{user_id}")
def get_tone_profile_endpoint(user_id: str):
    profile = get_tone_profile(user_id)
    if not profile:
        return {"error": "profile not found"}
    return profile
