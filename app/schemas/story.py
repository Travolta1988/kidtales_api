from app.schemas.story_settings import Language
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

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
    category: str
    full_story_context: str
    short_story_context: str
    reading_time_minutes: int
    is_favorite: bool

    class Config:
        from_attributes = True

# Story detail schema
class StoryDetailSchema(StoryListSchema):
    chapters: List[ChapterSchema] = []

    class Config:
        from_attributes = True

# Create story schema
class HeroId(str, Enum):
    princess = "princess"
    fox = "fox"
    dragon = "dragon"
    wizard = "wizard"
    cat = "cat"
    knight = "knight"
    fairy = "fairy"
    boy = "boy"
    girl = "girl"
    giant = "giant"

class LocationId(str, Enum):
    forest = "forest"
    castle = "castle"
    village = "village"
    mountain = "mountain"
    clouds = "clouds"
    cave = "cave"
    library = "library"
    oasis = "oasis"
    ice = "ice"
    garden = "garden"

class StyleId(str, Enum):
    andersen = "andersen"
    perrault = "perrault"
    grimm = "grimm"
    comic = "comic"
    bedtime = "bedtime"
    modern = "modern"

class StoryCreateRequest(BaseModel):
    language: Language
    hero: HeroId
    setting: LocationId
    style: StyleId

    class Config:
        from_attributes = True

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