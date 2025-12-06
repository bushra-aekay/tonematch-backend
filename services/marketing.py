#generating posts
from fastapi import HTTPException, status
from db.marketing_outputs import update_generated_posts, save_generated_posts
from db.business_profiles import save_business_profile

# can turn this into content_worker similar to strategy_worker
def process_post_generation(user_id: str, project_id: str, batch_id:str ,platforms: list[str], strategy_selected: str, business_profile: dict, tone_profile: dict):
    print("process started")
    posts = None
    try:
        posts = generate_posts(user_id, batch_id, strategy_selected, business_profile, tone_profile, platforms)
        update_generated_posts(batch_id, "COMPLETED", posts)
        save_business_profile(user_id, project_id, {"currentSelectedChannels": platforms})
        return {"batch_id": batch_id, "posts": posts}
    except Exception as e:
        if 'batch_id' in locals():
            update_generated_posts(batch_id, "FAILED")
        raise HTTPException(status_code=500, detail=f"Post generation failed: {e}")
    #updating current selected channels in business profiles
#mock

def generate_posts(user_id: str, batch_id: str, strategy_selected: str, business_profile:dict, tone_profile: dict, platforms: list[str]) -> dict:
    update_generated_posts(batch_id, "IN_PROGRESS")
    outputs = {} #dict mapping each channel to generated post
    for platform in platforms:
        platform_posts = [
            {
                "platform": platform,
                "text": f"Post 1: Thought leadership content idea for {platform} based on {business_profile['short_desc']}.",
                "tone": "abc",
                "keywords": "abcd"
            },
            {
                "platform": platform,
                "text": f"Post 2: Thought leadership content idea for {platform} based on {business_profile['short_desc']}.",
                "tone": "abc",
                "keywords": "abcd"
            },
        ]
        outputs[platform] = platform_posts
    
    return outputs

# from utils.claude_llm import generate_texts

# def generate_posts(user_id: str, business_profile:dict, tone_profile: dict, channels: list[str]):
#     outputs = {}
#     for channel in channels:
#         prompt =  f"""
#             You are a marketing assistant. Using the following:
#             Business Summary: {business_profile.get('business_summary', 'N/A')}
#             Tone: {tone_profile.get('styleSummary', 'casual')}
#             Target Audience: {business_profile.get('targetAudience', {})}
#             Channel: {channel}
#             Generate a short, engaging post formatted for this platform.
#             """
#         try: 
#             outputs[channel] = generate_texts(prompt)
#         except Exception as e: 
#             outputs[channel] = f"[{channel}] failed to generate post {str(e)}"
#     return outputs


def generate_suggested_strategy(user_id, business_profile:dict, tone_profile: dict):
    return {
        "channels": ["Instagram", "LinkedIn", "Twitter"],
        "tone": "Casual, humorous, engaging",
        "contentIdeas": ["Post about product launch", "Share user testimonial", "Run trending challenge"]
    }

# def generate_suggested_strategy(user_id, business_profile:dict, tone_profile: dict):
#         prompt = f"""
#         You are an expert marketing assistant.
#         Given the following business profile:
#         {business_profile}

#         And the user's tone profile:
#         {tone_profile}

#         Suggest a marketing strategy including:
#         - Best platforms/channels to post
#         - Tone/style to use
#         - 3-5 content ideas

#         Return only JSON with keys: channels (list), tone (string), contentIdeas (list of strings)
#         """
#         strategy = generate_texts(prompt)
#         return strategy