from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Categories(str, Enum):
    "fantasy",
    "adventure",
    "mystery",
    "horror",
    "romance",
    "science fiction",
    "dystopian",

class AIStoryOption(BaseModel):
    id: str
    text: str

    class Config:
        from_attributes = True

class AIGeneratedChapterList(BaseModel):
    id: int
    chapter_number: int
    title: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=100, 
        description="Chapter title in format 'Chapter {chapter_number}: ...'"
    )
    content: str
    chapter_description: str
    next_options: List[AIStoryOption] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    class Config:
        from_attributes = True        

class AIGeneratedStoryResponse(BaseModel):
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
    chapters: List[AIGeneratedChapterList] = []
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class AIGeneratedChapterResponse(BaseModel):
    title: str
    content: str 
    chapter_description: str
    full_story_context: str
    next_options: List[AIStoryOption] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    class Config:
        from_attributes = True
        