from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv() #loading env variables

from routes import tone, business, posts, auth

app = FastAPI() #creating FastAPI server instance

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # add production frontend URL here when deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(tone.router)
app.include_router(business.router)
app.include_router(posts.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


# from pydantic import BaseModel
# from services.tone import analyze_tone
# from db.tone_profiles import get_tone_profile
# from db.business_profiles import save_business_profile, get_business_profile
# from services.marketing import generate_posts


# class ToneRequest(BaseModel): #defines the expected structure and validates the incoming data
#     user_id: str
#     posts: list[str]

# class BusinessProfileReq(BaseModel):
#     user_id: str
#     businessName: str
#     shortDescription: str
#     websiteLink: str | None = None
#     targetAudience: dict | None = None
#     currentMarketing: str | None = None
#     platfromsUsed: list[str] | None = None
#     brandKeywords: list[str] | None = None
#     voice: str | None = None

# class GeneratePostsReq(BaseModel):
#     user_id: str
#     channels: list[str]

# @app.post("/analyze-tone") #api endpoint
# def analyze_tone_result(request: ToneRequest): #function and request is the name/reference of the incoming data
#     result = analyze_tone(request.posts, request.user_id)
#     return result

# @app.get("/get-tone-profile/{user_id}")
# def get_tone_profile_endpoint(user_id: str):
#     profile = get_tone_profile(user_id)
#     if not profile:
#         return {"error": "profile not found"}
#     return profile


# @app.post("/save-business-profile")
# def save_business_profile_endpoint(request: BusinessProfileReq):
#     profile_data = request.dict()
#     user_id = profile_data.pop("user_id")

#     if "aiSuggestedStrategy" not in profile_data:
#         profile_data["aiSuggestedStrategy"] = {
#             "channels": ["Instagram", "LinkedIn", "Twitter"],
#             "tone": "Casual, humorous, engaging",
#             "contentIdeas": ["Post about product launch", "Share user testimonial", "Run trending challenge"]
#         }
#     save_business_profile(user_id, profile_data)
#     return {"message": "successfully saved"}

# @app.get('/get-business-profile/{user_id}')
# def get_business_profile_endpoint(user_id: str):
#     profile = get_business_profile(user_id)
#     if not profile:
#         return {"error": "profile not found"}
#     return profile
    
# @app.post("/generate-posts")
# def generate_posts_endpoint(request: GeneratePostsReq):
#     user_id = request.user_id
#     channels = request.channels
#     business_profile = get_business_profile(user_id)
#     if not business_profile:
#         return {"error": "no business profile found"}
#     tone_profile = get_tone_profile(user_id)
#     if not tone_profile:
#         return {"error": "no tone profile found"}
#     posts = generate_posts(user_id, business_profile, tone_profile, channels)
#     return {"generated_posts": posts}
