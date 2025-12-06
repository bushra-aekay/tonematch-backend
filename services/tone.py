#contains tone analysis logic
from utils.openai_llm import extract_tone_llm
from db.tone_profiles import save_tone_profile, get_tone_profile

def analyze_tone(posts: list[str], user_id: str) -> dict:
    if not posts:
        return {"error": "no posts provided"}
    combined_text = "\n".join(posts)
    tone_data = extract_tone_llm(combined_text)
    save_tone_profile(user_id, tone_data)

    return tone_data
    

# from transformers import pipeline

# sentiment_pipeline = pipeline(
#     "sentiment-analysis",
#     model="distilbert-base-uncased-finetuned-sst-2-english"
# )

# def analyze_tone(text: str):
#     result = sentiment_pipeline(text)
#     label = result[0]['label']
#     score = result[0]['score']

#     return {
#         "tone":label,
        
#     }

# def analyze_tone(post: list[str]) -> dict:
    
#     return{
#         "toneDimensions": {
#             "formal": 0.2,
#             "casual": 0.9,
#             "humorous": 0.7,
#             "serious": 0.3,
#             "controversial": 0.4,
#             "factual": 0.6,
#         },
#         "writingFeatures": {
#             "avgSentenceLength": 12,
#             "questionFrequency": 0.3,
#             "audienceAddress": "personal"
#         },
#         "styleSummary": "Causal, humorous tone with moderate factual depth"
#     }