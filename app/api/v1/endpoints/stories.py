import uuid
import models
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.story import StoryListSchema, StoryDetailSchema, StoryCreateRequest, StoryUpdateRequest, ChapterListSchema
from sqlalchemy.orm import Session
from app.services.ai_service import ai_service
from typing import List
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


### Get all stories: GET /api/v1/stories ###
@router.get("/", response_model=List[StoryListSchema])
async def get_all_stories(db: Session = Depends(get_db)):
    stories = db.query(models.Story).all()
    return stories

### Get a story by id: GET /api/v1/stories/{story_id} ###
@router.get("/{story_id}", response_model=StoryDetailSchema)
def get_story_by_id(story_id: str, db: Session = Depends(get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Story not found"
        )
    return story

### Update a story: PATCH /api/v1/stories/{story_id} ###
@router.patch("/{story_id}", response_model=StoryDetailSchema)
def update_story(story_id: str, payload: StoryUpdateRequest, db: Session = Depends(get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Story not found"
        )
    story.title = payload.title
    story.description = payload.description
    # db.commit()
    return story    

### Create a story: POST /api/v1/stories ###
@router.post("/", response_model=StoryDetailSchema)
async def create_story(payload: StoryCreateRequest, db: Session = Depends(get_db)):
    try:
        story = await ai_service.generate_story(
            hero=payload.hero,
            setting=payload.setting,
            style=payload.style
        )

        new_story = models.Story(
            id=str(uuid.uuid4()),
            title=story.title,
            author=story.author,
            category=story.category,
            summary=story.summary,
            reading_time_minutes=story.reading_time_minutes,
            emoji=story.emoji,
            accent_color=story.accent_color,
            is_favorite=story.is_favorite,
            chapters=[models.StoryChapter(content=chapter.content) for chapter in story.chapters],
            created_at=story.created_at,
        )

        db.add(new_story)
        db.commit()

        return new_story
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

### Delete a story: DELETE /api/v1/stories/{story_id} ###
@router.delete("/{story_id}", response_model=StoryDetailSchema)
def delete_story(story_id: str, db: Session = Depends(get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Story not found"
        )
    db.delete(story)
    db.commit()
    return story

### Generate next chapter for a story: POST /api/v1/stories/{story_id}/continue ###
@router.post("/{story_id}/continue", response_model=ChapterListSchema)
async def generate_next_chapter(story_id: str, db: Session = Depends(get_db)):
    chapter = db.query(models.StoryChapter).filter(models.StoryChapter.story_id == story_id).all()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chapter not found"
        )
    # chapter = await ai_service.generate_next_chapter(
    #     story_id=story_id,
    #     chapter_id=chapter.id
    # )
    return chapter

### Get all chapters of story: GET /api/v1/stories/{story_id}/chapters ###
@router.get("/{story_id}/chapters", response_model=List[ChapterListSchema])
def get_all_chapters(story_id: str, db: Session = Depends(get_db)):
    chapters = db.query(models.StoryChapter).filter(models.StoryChapter.story_id == story_id).all()
    print(chapters)
    return chapters

### Get chapter of story by ID: GET /api/v1/stories/{story_id}/chapters/{chapter_id} ###
@router.get("/{story_id}/chapters/{chapter_id}", response_model=ChapterListSchema)
def get_chapter_by_id(story_id: str, chapter_id: str, db: Session = Depends(get_db)):
    chapter = db.query(models.StoryChapter).filter(models.StoryChapter.story_id == story_id, models.StoryChapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chapter not found"
        )
    return chapter

### Add/Remove story from favorites: POST /api/v1/stories/{story_id}/toggle-favorites ###
@router.post("/{story_id}/toggle-favorites", response_model=StoryDetailSchema)
def toogle_favorites(story_id: str, db: Session = Depends(get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Story not found"
        )
    story.is_favorite = not story.is_favorite
    # db.commit()
    return story