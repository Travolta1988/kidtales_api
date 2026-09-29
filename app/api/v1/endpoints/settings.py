from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.story_settings import Language, StorySettingsSchema
from app.services.story_settings_service import StorySettingsService
import app.database.models as models

router = APIRouter()


def get_story_settings_service(db: Session = Depends(get_db)) -> StorySettingsService:
    return StorySettingsService(db)


### Get story settings for a language: GET /api/v1/settings/{language} ###
@router.get("/{language}", response_model=StorySettingsSchema)
def get_story_settings(
    language: Language,
    story_settings_service: StorySettingsService = Depends(get_story_settings_service),
) -> StorySettingsSchema:
    return story_settings_service.get_story_settings(language)
