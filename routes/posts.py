#routes/posts.py
# from db.tone_profiles import get_tone_profile
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from models.posts import GeneratePostsReq
from db.business_profiles import save_business_profile
from services.marketing import generate_posts, process_post_generation
from dependencies.profile import get_profiles_dependency
from db.marketing_outputs import save_generated_posts, get_post_batch_by_id
from dependencies.auth import get_current_user, extract_user_id
from typing import Dict, Any




router = APIRouter(
    prefix="/posts", 
    tags=['Posts']
)

@router.post("/generate-posts")
def generate_posts_endpoint(
    request: GeneratePostsReq,
    background_tasks: BackgroundTasks,
    user_id: str = Depends(extract_user_id),
    # profiles: dict = Depends(get_profiles_dependency, use_cache=False), # FastAPI handles all fetching/validation 
    ):    
    profiles = get_profiles_dependency(request.project_id, user_id)
    business_profile = profiles["business"]
    tone_profile = profiles["tone"]
    batch_id = save_generated_posts(user_id, request.project_id, request.platforms, status="PENDING")
    background_tasks.add_task(
        process_post_generation,
        user_id,
        request.project_id,
        batch_id,
        request.platforms,
        request.strategy_selected,
        business_profile,
        tone_profile,
    )
    return {"batch_id": batch_id, "status": "PENDING"}
    # user_id = user_data.get('user_id')
    # platforms = request.platforms
    # calling AI post generator
    # profiles = get_profiles_dependency(request.project_id, user_id)
    # posts = None
    # try:
    #     batch_id = save_generated_posts(user_id, project_id, request.platforms, status="PENDING")
    #     posts = generate_posts(user_id, batch_id, request.strategy_selected, business_profile, tone_profile, platforms)
    # saving generated posts to db, and getting batch id  
    # return {"generated_posts": posts, "batch_id": batch_id, "message":"posts generated and saved to history."}

@router.get('/get-posts/{batch_id}')
def get_posts_endpoint(batch_id: str):
    batch_data = get_post_batch_by_id(batch_id)
    if not batch_data:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch_data

# @router.post('/generate-strategy/{user_id}')
# def generate_strategy_endpoint(
#     user_id: str,
#     profiles: dict = Depends(get_profiles_dependency, use_cache=False)    
#     ):
#     business_profile = profiles["business"]
#     tone_profile = profiles["tone"]
#     suggested_strategy = generate_strategy_endpoint(user_id, business_profile, tone_profile)
#     business_profile["aiSuggestedStrategy"] = suggested_strategy
#     save_business_profile(user_id, business_profile)
#     return {"message": "AI strategy generated and saved successfully."}