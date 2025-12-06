# routes/business.py
from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Depends, Path
# from pydantic import BaseModel
from db.business_profiles import get_business_profile, create_new_project
from services.strategy_worker import generate_strategy_worker
from models.business import BusinessProfile
from typing import Dict, Any
from dependencies.auth import get_current_user


router = APIRouter(
    prefix="/business", 
    tags=['Business']
)


@router.get('/{project_id}')
async def get_business_profile_endpoint( 
    project_id: str = Path(...,description="The ID of the business project to fetch"),
    user_data: Dict[str, Any] = Depends(get_current_user)
    ):
    user_id = user_data.get('user_id')
    document = get_business_profile(user_id, project_id)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    return document


@router.post("/save-business-profile")
async def save_business_profile_endpoint(
    request: BusinessProfile, 
    background_tasks: BackgroundTasks,
    user_data: Dict[str, Any] = Depends(get_current_user),
    ):
    user_id = user_data.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User ID not found in session data.")
    profile_data = request.dict()
    project_id = create_new_project(user_id, profile_data)
    
    background_tasks.add_task(generate_strategy_worker, user_id, project_id)
    
    return {"id": str(project_id)}




  # if "aiSuggestedStrategy" not in profile_data:
    #     profile_data["aiSuggestedStrategy"] = {
    #         "channels": ["Instagram", "LinkedIn", "Twitter"],
    #         "tone": "Casual, humorous, engaging",
    #         "contentIdeas": ["Post about product launch", "Share user testimonial", "Run trending challenge"]
    #     }