from pydantic import BaseModel, Field

class ToneRequest(BaseModel): #defines the expected structure and validates the incoming data
    # user_id: str
    posts: list[str] = Field(..., min_items=3, max_items=5, description="A list of 3 to 5 raw text examples for tone analysis.")
