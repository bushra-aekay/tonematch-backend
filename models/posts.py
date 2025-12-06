from pydantic import BaseModel
class GeneratePostsReq(BaseModel):
    # user_id: str
    project_id: str
    strategy_selected: str
    platforms: list[str]

