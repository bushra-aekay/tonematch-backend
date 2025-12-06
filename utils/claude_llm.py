import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_texts(prompt: str, max_tokens: int = 300):
    response = client.completions.create(
        model="claude-2",
        prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
        max_tokens_to_sample=max_tokens,
    )
    return response.completion