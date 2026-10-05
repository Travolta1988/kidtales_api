from app.schemas.story import ChapterSchema
import json
import uuid
from collections.abc import AsyncIterator
from datetime import datetime
import app.database.models as models
import logging
from app.core.errors import ERRORS, AI_ERRORS
from fastapi import Depends, HTTPException, status, BackgroundTasks
from app.schemas.story import StoryListSchema, StoryDetailSchema, StoryUpdateRequest, ChapterListSchema, StoryOptionSchema
from app.schemas.story_settings import ResolvedStoryInput
from sqlalchemy.orm import Session
from app.services.ai_service import ai_service, AIError
from typing import List
from app.database.database import get_db, SessionLocal
from app.services.generate_cover_image import build_flux_prompt, save_cover

logger = logging.getLogger(__name__)

def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

class StoryService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db 

    ### SERVICE METHODS ###
    def ensure_credits(self, user: models.User) -> None:
        if user.subscription_credits + user.purchased_credits < 1:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=ERRORS["INSUFFICIENT_CREDITS_ERROR"]
            )         

    ### CRUD METHODS ###
    # get_all_stories -> List[StoryListSchema]
    # get_story_by_id -> StoryDetailSchema
    # update_story -> StoryDetailSchema
    # delete_story -> None
    # get_all_chapters -> List[ChapterListSchema]
    # get_chapter_by_id -> ChapterListSchema
    # toogle_favorites -> StoryDetailSchema

    ### Get all stories ###
    def get_all_stories(self, user: models.User) -> List[StoryListSchema]:
        return self.db.query(models.Story).filter(models.Story.user_id == user.id).all()

    ### Get a story by id ###
    def get_story_by_id(self, story_id: str, user: models.User) -> StoryDetailSchema:
        story = self.db.query(models.Story).filter(models.Story.id == story_id, models.Story.user_id == user.id).first()
        if not story:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ERRORS["STORY_NOT_FOUND_ERROR"]
            )
        return story

    ### Update a story ###
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

    ### Delete a story ###
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

    ### Get all chapters ###
    def get_all_chapters(self, story_id: str, user: models.User) -> List[ChapterListSchema]:
        return self.db.query(models.StoryChapter).filter(models.StoryChapter.story_id == story_id).all()
    
    ### Get a chapter by id ###
    def get_chapter_by_id(self, story_id: str, chapter_id: str, user: models.User) -> ChapterListSchema:
        chapter = self.db.query(models.StoryChapter).filter(models.StoryChapter.story_id == story_id, models.StoryChapter.id == chapter_id).first()
        if not chapter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=ERRORS["CHAPTER_NOT_FOUND_ERROR"]
            )
        return chapter

    ### Toggle favorites ###
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

    # STREAMING METHODS #
    # stream_create_story -> AsyncIterator[str]
    # generate_next_chapter -> AIGeneratedChapterResponse

    ### Create a story ###
    async def stream_create_story(
        self,
        user: models.User,
        payload: ResolvedStoryInput,
        cover_image_generation_payload,
        background_tasks: BackgroundTasks,
    ) -> AsyncIterator[str]:
        story_stream = ai_service.stream_story(
            hero=payload.hero,
            setting=payload.setting,
            style=payload.style,
            language=payload.language,
        )

        try:
            async for delta in story_stream:
                yield _sse({"delta": delta})
        except AIError:
            logger.exception("AI error while generating story")
            yield _sse({"error": AI_ERRORS["AI_ERROR"]})
            return

        story = story_stream.parsed
        if story is None or not story.chapters:
            logger.warning("AI returned an empty story")
            yield _sse({"error": AI_ERRORS["AI_ERROR"]})
            return

        if user.subscription_credits > 0:
            user.subscription_credits -= 1
        elif user.purchased_credits > 0:
            user.purchased_credits -= 1
        else:
            yield _sse({"error": ERRORS["INSUFFICIENT_CREDITS_ERROR"]})
            return  

        new_story = models.Story(
            id=str(uuid.uuid4()),
            user_id=user.id,
            title=story.title,
            hero=payload.hero,
            setting=payload.setting,
            style=payload.style,
            generated_chapters_count=len(story.chapters),
            image_url=None,
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
            background_tasks.add_task(
                save_cover, 
                new_story.id, 
                build_flux_prompt(
                    cover_image_generation_payload.hero, 
                    cover_image_generation_payload.setting
                )
            )
            self.db.refresh(new_story)
        except Exception:
            self.db.rollback()
            logger.exception("Error while saving story to database")
            yield _sse({"error": ERRORS["STORY_GENERATION_ERROR"]})
            return

        detail = StoryDetailSchema.model_validate(new_story)
        yield _sse({"story": detail.model_dump(mode="json")})

    ### Generate a next chapter ###
    async def stream_create_next_chapter(self, story_id: str, user: models.User, payload: StoryOptionSchema) -> AsyncIterator[str]:
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
            stream_chapter = await ai_service.stream_chapter_conclusion(
                hero=story.hero,
                setting=story.setting,
                style=story.style,
                full_story_context=story.full_story_context,
                chapter_number=10,
                previous_chapter_content=last_chapter.content,
                chapter_description=last_chapter.chapter_description
            )
        else:
            stream_chapter = await ai_service.stream_chapter_next(
                hero=story.hero,
                setting=story.setting,
                full_story_context=story.full_story_context,
                style=story.style,
                chapter_number=next_number,
                previous_chapter_content=last_chapter.content,
                chapter_description=last_chapter.chapter_description,
                next_option=payload.text,
            )

        try:
            async for delta in stream_chapter:
                yield _sse({"delta": delta})
        except AIError:
            logger.exception("AI error while generating chapter")
            yield _sse({"error": AI_ERRORS["AI_ERROR"]})
            return   

        new_chapter = stream_chapter.parsed
        if new_chapter is None:
            logger.warning("AI returned an empty chapter")
            yield _sse({"error": AI_ERRORS["AI_ERROR"]})
            return  

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

        record = models.StoryChapter(
            story_id=story_id,
            chapter_number=next_number,
            content=new_chapter.content,
            title=new_chapter.title,
            chapter_description=new_chapter.chapter_description,
            next_options=[opt.model_dump() for opt in new_chapter.next_options],
        )   

        story.full_story_context = new_chapter.full_story_context
        story.chapters.append(record)
        story.generated_chapters_count = len(story.chapters)
        # Save new chapter to database
        try:
            self.db.commit()
            self.db.refresh(story)
            self.db.refresh(record)
            self.db.refresh(user)
        except Exception:
            self.db.rollback()
            logger.exception("Error while saving chapter to database")
            yield _sse({"error": ERRORS["CHAPTER_GENERATION_ERROR"]})
            return

        detail = ChapterSchema.model_validate(record)
        yield _sse({"chapter": detail.model_dump(mode="json")})    