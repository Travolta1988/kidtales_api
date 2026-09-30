import uuid
from datetime import datetime
import app.database.models as models
import logging
from app.core.errors import ERRORS, AI_ERRORS
from fastapi import Depends, HTTPException, status
from app.schemas.story import StoryListSchema, StoryDetailSchema, StoryUpdateRequest, ChapterListSchema, StoryOptionSchema
from app.schemas.ai import AIGeneratedChapterResponse
from app.schemas.story_settings import ResolvedStoryInput
from sqlalchemy.orm import Session
from app.services.ai_service import ai_service, AIError
from typing import List
from app.database.database import get_db

logger = logging.getLogger(__name__)

class StoryService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db   

    def get_all_stories(self, user: models.User) -> List[StoryListSchema]:
        return self.db.query(models.Story).filter(models.Story.user_id == user.id).all()

    def get_story_by_id(self, story_id: str, user: models.User) -> StoryDetailSchema:
        story = self.db.query(models.Story).filter(models.Story.id == story_id, models.Story.user_id == user.id).first()
        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ERRORS["STORY_NOT_FOUND_ERROR"]
            )
        return story

    def update_story(self, story_id: str, payload: StoryUpdateRequest, user: models.User) -> StoryDetailSchema:
        story = self.db.query(models.Story).filter(models.Story.id == story_id, models.Story.user_id == user.id).first()
        
        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ERRORS["STORY_NOT_FOUND_ERROR"]
            )
        story.title = payload.title
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            logger.exception("Error while updating story in database")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=ERRORS["STORY_UPDATE_ERROR"]
            )
        self.db.refresh(story)
        return story

    async def create_story(self, user: models.User, payload: ResolvedStoryInput) -> StoryDetailSchema:
        # Check if user has sufficient credits
        if user.subscription_credits + user.purchased_credits < 1:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=ERRORS["INSUFFICIENT_CREDITS_ERROR"]
            )
        try:
            story = await ai_service.generate_story(
                hero=payload.hero,
                setting=payload.setting,
                style=payload.style,
                language=payload.language,
            )
        except AIError:
            logger.exception("AI error while generating story")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=AI_ERRORS["AI_ERROR"]
            )

        if story is None or not story.chapters:
            logger.warning("AI returned an empty story")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=AI_ERRORS["AI_ERROR"],
            ) 

        # Withdraw 1 credit
        if user.subscription_credits > 0:
            user.subscription_credits -= 1
        elif user.purchased_credits > 0:
            user.purchased_credits -= 1
        else:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=ERRORS["INSUFFICIENT_CREDITS_ERROR"]
            )     

        new_story = models.Story(
            id=str(uuid.uuid4()),
            user_id=user.id,
            title=story.title,
            hero=payload.hero,
            setting=payload.setting,
            style=payload.style,
            category=story.category,
            full_story_context=story.full_story_context,
            short_story_context=story.short_story_context,
            reading_time_minutes=story.reading_time_minutes,
            is_favorite=False,
            created_at=story.created_at or datetime.now(),
            chapters=[
                models.StoryChapter(
                    chapter_number=index,
                    title=chapter.title,
                    content=chapter.content,
                    chapter_description=chapter.chapter_description,
                    next_options=[opt.model_dump() for opt in chapter.next_options],
                )
                for index, chapter in enumerate(story.chapters, start=1)
            ],
        )

        try:
            self.db.add(new_story)
            self.db.commit()
            self.db.refresh(new_story)
        except Exception:
            self.db.rollback()
            logger.exception("Error while saving story to database")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=ERRORS["STORY_GENERATION_ERROR"]
            )

        return new_story

    def delete_story(self, story_id: str, user: models.User) -> None:
        story = self.db.query(models.Story).filter(models.Story.id == story_id).first()
        
        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ERRORS["STORY_NOT_FOUND_ERROR"]
            )

        try:    
            self.db.delete(story)
            self.db.commit()
        except Exception:
            self.db.rollback()
            logger.exception("Error while deleting story from database")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=ERRORS["STORY_DELETION_ERROR"]
            )   

    async def generate_next_chapter(self, story_id: str, user: models.User, payload: StoryOptionSchema) -> AIGeneratedChapterResponse:
        # Check if user has sufficient credits
        if user.subscription_credits + user.purchased_credits < 1:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=ERRORS["INSUFFICIENT_CREDITS_ERROR"]
            )
        story: models.Story | None = self.db.query(models.Story).filter(models.Story.id == story_id, models.Story.user_id == user.id).first()

        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ERRORS["STORY_NOT_FOUND_ERROR"]
            )

        if not story.chapters:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ERRORS["STORY_NO_CHAPTERS_ERROR"]
            )

        last_chapter = max(story.chapters, key=lambda c: c.chapter_number)
        next_number = last_chapter.chapter_number + 1

        if last_chapter.chapter_number >= 10:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ERRORS["STORY_ALREADY_CONCLUDED_ERROR"]
            )

        if next_number == 10:
            chapter = await ai_service.generate_story_conclusion(
                hero=story.hero,
                setting=story.setting,
                style=story.style,
                full_story_context=story.full_story_context,
                chapter_number=10,
                previous_chapter_content=last_chapter.content,
                chapter_description=last_chapter.chapter_description
            )
        else:
            chapter = await ai_service.generate_next_chapter(
                hero=story.hero,
                setting=story.setting,
                full_story_context=story.full_story_context,
                style=story.style,
                chapter_number=next_number,
                previous_chapter_content=last_chapter.content,
                chapter_description=last_chapter.chapter_description,
                next_option=payload.text,
            )

        new_chapter = AIGeneratedChapterResponse(
            content=chapter.content,
            chapter_description=chapter.chapter_description,
            title=chapter.title,
            full_story_context=chapter.full_story_context,
            next_options=[opt.model_dump() for opt in chapter.next_options],
        )

        record = models.StoryChapter(
            story_id=story_id,
            chapter_number=next_number,
            content=new_chapter.content,
            title=new_chapter.title,
            chapter_description=new_chapter.chapter_description,
            next_options=[opt.model_dump() for opt in new_chapter.next_options],
        )

        # Withdraw 1 credit
        if user.subscription_credits > 0:
            user.subscription_credits -= 1
        elif user.purchased_credits > 0:
            user.purchased_credits -= 1
        else:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=ERRORS["INSUFFICIENT_CREDITS_ERROR"]
            )     

        story.full_story_context = new_chapter.full_story_context

        # Save new chapter to database
        try:
            self.db.add(record)
            self.db.commit()
            self.db.refresh(story)
            self.db.refresh(user)
        except Exception:
            self.db.rollback()
            logger.exception("Error while saving story to database")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=ERRORS["CHAPTER_GENERATION_ERROR"]
            )

        return new_chapter

    def get_all_chapters(self, story_id: str, user: models.User) -> List[ChapterListSchema]:
        return self.db.query(models.StoryChapter).filter(models.StoryChapter.story_id == story_id).all()

    def get_chapter_by_id(self, story_id: str, chapter_id: str, user: models.User) -> ChapterListSchema:
        chapter = self.db.query(models.StoryChapter).filter(models.StoryChapter.story_id == story_id, models.StoryChapter.id == chapter_id).first()
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ERRORS["CHAPTER_NOT_FOUND_ERROR"]
            )
        return chapter

    def toogle_favorites(self, story_id: str, user: models.User) -> StoryDetailSchema:
        story = self.db.query(models.Story).filter(models.Story.id == story_id).first()
        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ERRORS["STORY_NOT_FOUND_ERROR"]
            )
        story.is_favorite = not story.is_favorite
        self.db.commit()
        self.db.refresh(story)
        return story