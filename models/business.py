# models/business

from pydantic import BaseModel, Field
from typing import Optional

class BusinessProfile(BaseModel):
    # user_id: str --> handled by auth, not req body
    name: str  = Field(..., description="The name of the business or project.")
    industry: str | None = Field(None, description="The industry or niche of the business.")
    target_audience: str = Field(..., description="Detailed description of the target customer.")
    # target_audience: dict | None = None
    mission: str | None = Field(None, description="The core business mission or value proposition.")
    short_desc: str = Field(..., description="A short description of what the business actually does")
    website_link: str | None = Field(None, description="Link of the website")
    current_marketing: str | None = Field(None, description="Current marketing strategies")
    platforms_currently_used: list[str] | None = Field(None, description="List of platforms currently used for marketing")
    brand_keywords: list[str] | None = Field(None, description="List of keywords that brand represents or is represented by")
    voice: str | None = Field(None, description="A detailed description of the brand's voice (e.g., 'Witty and sarcastic, but professional').")
    ai_strategy_status: str = Field("PENDING", description="Status of the AI strategy generation (PENDING, COMPLETED, FAILED)")
    ai_suggested_strategy: Optional[dict] = Field(None, description="The final generated strategy structure")
# ok we need to add project id/ business id - whichever is less confusing, and add industry and mission in this
# we can add shortdesc, websiteLink, currentMarketing, platformsCurrentlyUsed, brandKeywords, voice and userId from frontend?

