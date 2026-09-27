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
    author: str
    hero: str
    setting: str
    style: str
    category: str
    full_story_context: str
    reading_time_minutes: int
    emoji: str
    is_favorite: bool

    class Config:
        from_attributes = True

# Story detail schema
class StoryDetailSchema(StoryListSchema):
    chapters: List[ChapterSchema] = []

    class Config:
        from_attributes = True

# Create story schema
class StoryCreateRequest(BaseModel):
    hero: str
    setting: str
    style: str

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

# AI Model schemas
class StoryResponse(BaseModel):
    id: str
    title: str
    author: str
    hero: str
    setting: str
    style: str
    category: str
    full_story_context: str
    reading_time_minutes: int
    emoji: str
    is_favorite: bool
    chapters: List[ChapterListSchema] = []
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class ChapterGenerationSchema(BaseModel):
    title: str
    content: str 
    chapter_description: str
    full_story_context: str
    next_options: List[StoryOptionSchema] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    class Config:
        from_attributes = True



# Generation schemas
class GeneratedOption(BaseModel):
    id: str
    text: str

class GeneratedChapter(BaseModel):
    title: str
    content: str
    chapter_description: str
    next_options: List[GeneratedOption] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

class GeneratedStory(BaseModel):
    title: str
    author: str
    category: str
    emoji: str
    reading_time_minutes: int
    full_story_context: str
    chapters: list[GeneratedChapter]        