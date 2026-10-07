from app.schemas.story_settings import Language
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class HeroId(str, Enum):
    hedgehog_inventor = "hedgehog_inventor"
    kind_robot = "kind_robot"
    star_raccoon = "star_raccoon"
    flying_whale = "flying_whale"
    steampunk_dino = "steampunk_dino"
    living_toy = "living_toy"
    owl_storyteller = "owl_storyteller"
    magician_fox = "magician_fox"

class LocationId(str, Enum):
    night_express = "night_express"
    treehouse = "treehouse"
    cloud_planet = "cloud_planet"
    airship = "airship"
    underwater_shell_city = "underwater_shell_city"
    starlight_camp = "starlight_camp"
    clockmaker_shop = "clockmaker_shop"
    living_drawings_world = "living_drawings_world"


class StyleId(str, Enum):
    bedtime_story = "bedtime_story"
    funny_adventure = "funny_adventure"
    cozy_classic = "cozy_classic"
    cartoon_magic = "cartoon_magic"
    interactive_quest = "interactive_quest"

# Next options schema
class StoryOptionSchema(BaseModel):
    id: str
    text: str

    class Config:
        from_attributes = True

# Chapter schema
class ChapterSchema(BaseModel):
    id: int
    chapter_number: int
    title: Optional[str] = None
    content: str
    chapter_description: str
    next_options: List[StoryOptionSchema] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    class Config:
        from_attributes = True

# Story list schema
class StoryListSchema(BaseModel):
    id: str
    title: str
    hero: str
    setting: str
    style: str
    goal: str
    language: Language
    generated_chapters_count: int
    image_url: Optional[str] = None
    category: str
    full_story_context: str
    short_story_context: str
    reading_time_minutes: int
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Story detail schema
class StoryDetailSchema(StoryListSchema):
    chapters: List[ChapterSchema] = []

    class Config:
        from_attributes = True

# Create story schema
class GoalId(str, Enum):
    fall_asleep = "fall_asleep"
    overcome_fear = "overcome_fear"
    friendship_sharing = "friendship_sharing"
    confidence_mistakes = "confidence_mistakes"
    curiosity_learning = "curiosity_learning"

class StoryCreateRequest(BaseModel):
    language: Language
    hero: HeroId
    setting: LocationId
    style: StyleId
    goal: GoalId

    class Config:
        from_attributes = True

class ContinueStoryRequest(BaseModel):
    id: str
    text: str
    language: Language
    hero: str
    setting: str
    style: str
    goal: str

# Update story schema
class StoryUpdateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)

    class Config:
        from_attributes = True

# Chapter list schema
class ChapterListSchema(BaseModel):
    id: int
    chapter_number: int
    title: Optional[str] = None
    content: str
    chapter_description: str
    next_options: List[StoryOptionSchema] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    class Config:
        from_attributes = True