import app.database.models as models
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.errors import ERRORS
from app.schemas.story_settings import (
    CatalogItemSchema,
    Language,
    ResolvedStoryInput,
    StorySettingsSchema,
)


class StorySettingsService:
    def __init__(self, db: Session):
        self.db = db

    def get_story_settings(self, language: Language) -> StorySettingsSchema:
        code = language.value
        row = (
            self.db.query(models.StorySettings)
            .filter(models.StorySettings.catalog.has_key(code))
            .first()
        )
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERRORS["STORY_SETTINGS_NOT_FOUND_ERROR"],
            )
        return StorySettingsSchema.model_validate(row.catalog[code])

    def resolve(
        self,
        language: Language,
        hero_id: str,
        setting_id: str,
        style_id: str,
    ) -> ResolvedStoryInput:
        catalog = self.get_story_settings(language)
        return ResolvedStoryInput(
            language=language,
            hero_id=hero_id,
            setting_id=setting_id,
            style_id=style_id,
            hero=self._title_for(catalog.heroes, hero_id, "hero"),
            setting=self._title_for(catalog.locations, setting_id, "setting"),
            style=self._title_for(catalog.styles, style_id, "style"),
        )

    @staticmethod
    def _title_for(items: list[CatalogItemSchema], item_id: str, field: str) -> str:
        for item in items:
            if item.id == item_id:
                return item.title
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown {field}: {item_id}",
        )
        
