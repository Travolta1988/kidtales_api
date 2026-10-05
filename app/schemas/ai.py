from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AIStoryOption(BaseModel):
    id: str
    text: str

    class Config:
        from_attributes = True

class AIGeneratedChapterList(BaseModel):
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
    id: int
    chapter_number: int

    class Config:
        from_attributes = True        

class AIGeneratedStoryResponse(BaseModel):
    chapters: List[AIGeneratedChapterList]
    title: str
    hero: str
    setting: str
    style: str
    category: str
    short_story_context: str
    full_story_context: str
    reading_time_minutes: int
    is_favorite: bool
    id: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class AIGeneratedChapterResponse(BaseModel):
    title: str
    content: str = Field(
        ..., 
        description="""
        Chapter content should be minimum 600 words and maximum 700 words.
        Content should not repeat the same information as the previous chapter.
        Content should be interesting with some humor and some action.
        """
    )
    chapter_description: str
    full_story_context: str
    next_options: List[AIStoryOption] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Next fields should not repeat the same options as the previous chapter."
    )

    class Config:
        from_attributes = True
        