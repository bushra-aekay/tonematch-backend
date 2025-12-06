from fastapi import HTTPException, Depends
from db.tone_profiles import get_tone_profile
from db.business_profiles import get_business_profile
from dependencies.auth import extract_user_id

# def get_user_id(user_id: str | None = None, request_body: dict | None = None):
#     if user_id:
#         return user_id
    
def get_profiles_dependency(
    project_id: str,
    user_id: str = Depends(extract_user_id), # Injected,
    ):
    business_profile = get_business_profile(user_id, project_id)
    tone_profile = get_tone_profile(user_id)

    if not business_profile:
        raise HTTPException(status_code=404, detail="Business profile not found")
    if not tone_profile:
        raise HTTPException(status_code=404, detail="Tone profile not found")
    return{
        "business": business_profile,
        "tone": tone_profile
    }