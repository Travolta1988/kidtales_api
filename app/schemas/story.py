from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Chapter schema
class ChapterSchema(BaseModel):
    id: int
    chapter_number: int
    title: Optional[str] = None
    content: str

    class Config:
        from_attributes = True

# Story list schema
class StoryListSchema(BaseModel):
    id: str
    title: str
    author: str
    category: str
    summary: str
    reading_time_minutes: int
    emoji: str
    accent_color: str
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
    title: str
    description: str

    class Config:
        from_attributes = True

# Chapter list schema
class ChapterListSchema(BaseModel):
    id: int
    chapter_number: int
    title: Optional[str] = None
    content: str

    class Config:
        from_attributes = True

# Update chapter schema
class ChapterUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: str

    class Config:
        from_attributes = True

# Delete chapter schema
class ChapterDeleteRequest(BaseModel):
    id: int

    class Config:
        from_attributes = True

class StoryResponse(BaseModel):
    id: str
    title: str
    author: str
    category: str
    summary: str
    reading_time_minutes: int
    emoji: str
    accent_color: str
    is_favorite: bool
    chapters: List[ChapterListSchema] = []
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True