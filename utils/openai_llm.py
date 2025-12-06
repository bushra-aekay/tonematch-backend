# Mock data

def extract_tone_llm(text: str) -> dict:
    return {
        "styleSummary": "Casual, humorous tone with moderate factual depth",
        "toneDimensions": {
            "formal": 0.2,
            "casual": 0.9,
            "humorous": 0.7,
            "serious": 0.3,
            "controversial": 0.4,
            "factual": 0.6
        },
        "writingFeatures": {
            "avgSentenceLength": 12,
            "questionFrequency": 0.3,
            "audienceAddress": "personal"
        }
    }




# from openai import OpenAI
# import os

# client = OpenAI() #creating openAi client instance
# #fn that sends texts -> openAi -> returns structured tone analysis
# def extract_tone_llm(text: str) -> dict:
#     #propmt to give to openAI
#     prompt = f"""Analyze the tone of the following text and provide
#                 a detailed breakdown of its tone dimensions and writing features:\n\n{text}\n\nProvide the analysis in JSON format with keys 'toneDimensions' 
#                 and 'writingFeatures'.
#                 Text: 
#                 {text}

#                 Extract: 
#                 - short style summary
#                 - tone dimensions with scores from 0 to 1 for aspects like formal, casual, humorous, serious, controversial, factual
#                 - writing features such as average sentence length, question frequency (0-1), audience address style (personal/neutral/expert)
#                 - any extra underlying information, relationships and context that might be relevant for deeper analysis under the key 'extraUnderlyingInfo'
                
#                 Respont ONLY using JSON with keys:
#                 styleSummary
#                 toneDimensions
#                 writingFeatures
#                 extraUnderlyingInfo
#                 """
#     #sending request to LLM
#     response = client.chat.completions.create(
#         model="gpt-5",
#         messages = [{"role": "user", "content": prompt}],
#         temperature=0.7,
#     )

#     #getting AI's raw response
#     raw = response.choices[0].message.content
    
#     #converting tect to JSON dict
#     import json
#     try: 
#         parsed = json.loads(raw)
#     except:
#         parsed = {
#             "styleSummary": raw,
#             "toneDimensions": {},
#             "writingFeatures": {},
#             "extraUnderlyingInfo": raw
#         }
#     return parsed
 