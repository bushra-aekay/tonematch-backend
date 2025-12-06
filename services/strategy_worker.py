#strategy worker to run in backgroun after business profile saving
from services.marketing import generate_suggested_strategy
from db.tone_profiles import get_tone_profile
from db.business_profiles import get_business_profile, update_project_strategy_success

def generate_strategy_worker(user_id: str, project_id: str):
    update_project_strategy_success(project_id, "IN_PROGRESS")

    try:
        business_profile = get_business_profile(user_id, project_id)
        tone_profile = get_tone_profile(user_id)
        if not business_profile or not tone_profile:
            update_project_strategy_success(project_id, "FAILED")
        suggested_strategy = generate_suggested_strategy(user_id, business_profile, tone_profile) #user-id is not really needed, maybe remove in future
        update_project_strategy_success(project_id, "COMPLETED", suggested_strategy)
    except Exception as e:
        print(f"Strategy generation failed for {project_id}: {e}")
        update_project_strategy_success(project_id, "FAILED")