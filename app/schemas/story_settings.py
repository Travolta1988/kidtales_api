from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Language(str, Enum):
    en = "en"
    uk = "uk"
    de = "de"


class CatalogItemSchema(BaseModel):
    id: str
    title: str
    hint: str
    color: int
    image: Optional[str] = None


class StorySettingsSchema(BaseModel):
    heroes: list[CatalogItemSchema]
    locations: list[CatalogItemSchema]
    styles: list[CatalogItemSchema]
    goals: list[CatalogItemSchema]


class ResolvedStoryInput(BaseModel):
    language: Language
    hero_id: str
    setting_id: str
    style_id: str
    goal_id: str
    hero: str
    setting: str
    style: str
    goal: str
