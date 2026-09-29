from enum import Enum

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


class StorySettingsSchema(BaseModel):
    heroes: list[CatalogItemSchema]
    locations: list[CatalogItemSchema]
    styles: list[CatalogItemSchema]


class ResolvedStoryInput(BaseModel):
    language: Language
    hero_id: str
    setting_id: str
    style_id: str
    hero: str
    setting: str
    style: str
