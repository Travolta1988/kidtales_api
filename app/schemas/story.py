from pydantic import BaseModel, Field
from typing import List

# Request tale creation
class StoryCreateRequest(BaseModel):
    hero_name: str = Field(..., example="Kai", description="Main hero name")
    setting: str = Field(..., example="Snow castle", description="Location/Setting")
    style: str = Field(default="Hans Christian Andersen", description="Fairy Tale style")

# 2. Model of future action variation
class StoryOption(BaseModel):
    option_id: int = Field(..., example=1, description="Variations (1, 2 or 3)")
    text: str = Field(..., example="Open ice door", description="Action description")

# 3. Response with generative chapter
class ChapterResponse(BaseModel):
    story_id: str = Field(..., example="story_12345", description="Fairy tale unique ID")
    chapter_number: int = Field(..., example=1, description="Current chapter number")
    title: str = Field(..., example="Северные Ветра", description="Chapter title")
    content: str = Field(..., description="Chapter content")
    options: List[StoryOption] = Field(..., min_items=3, max_items=3, description="Continue variations")

# 4. Selected variation request
class StoryNextStepRequest(BaseModel):
    selected_option_id: int = Field(..., example=1, ge=1, le=3, description="Selected variation from 1 to 3")