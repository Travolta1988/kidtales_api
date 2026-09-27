from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, status
from app.schemas.story import StoryListSchema, StoryDetailSchema, StoryCreateRequest, StoryUpdateRequest, ChapterListSchema, ChapterGenerationSchema, StoryOptionSchema
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.services.story_service import StoryService
import app.database.models as models

router = APIRouter()

def get_story_service(db: Session = Depends(get_db)) -> StoryService:
    return StoryService(db)

### Get all stories: GET /api/v1/stories ###
@router.get("/", response_model=List[StoryListSchema])
def get_all_stories(
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> List[StoryListSchema]:
    return story_service.get_all_stories(user=current_user)

### Get a story by id: GET /api/v1/stories/{story_id} ###
@router.get("/{story_id}", response_model=StoryDetailSchema)
def get_story_by_id(
    story_id: str, 
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> StoryDetailSchema:
    return story_service.get_story_by_id(story_id, user=current_user)

### Update a story: PATCH /api/v1/stories/{story_id} ###
@router.patch("/{story_id}", response_model=StoryDetailSchema)
def update_story(
    story_id: str, 
    payload: StoryUpdateRequest, 
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> StoryDetailSchema:
    return story_service.update_story(story_id, payload, user=current_user)

### Create a story: POST /api/v1/stories ###
@router.post("/", response_model=StoryDetailSchema)
async def create_story(
    payload: StoryCreateRequest,
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> StoryDetailSchema:
    return await story_service.create_story(payload, user=current_user)   

### Delete a story: DELETE /api/v1/stories/{story_id} ###
@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(
    story_id: str, 
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> None:
    story_service.delete_story(story_id, user=current_user)

### Generate next chapter for a story: POST /api/v1/stories/{story_id}/continue ###
@router.post("/{story_id}/continue", response_model=ChapterGenerationSchema)
async def generate_next_chapter(
    story_id: str,
    payload: StoryOptionSchema,  # <- Принимаем тело запроса с опцией продолжения
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> ChapterGenerationSchema:
    return await story_service.generate_next_chapter(story_id, user=current_user, payload=payload)

### Get all chapters of story: GET /api/v1/stories/{story_id}/chapters ###
@router.get("/{story_id}/chapters", response_model=List[ChapterListSchema])
def get_all_chapters(
    story_id: str, 
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> List[ChapterListSchema]:
    return story_service.get_all_chapters(story_id, user=current_user)

### Get chapter of story by ID: GET /api/v1/stories/{story_id}/chapters/{chapter_id} ###
@router.get("/{story_id}/chapters/{chapter_id}", response_model=ChapterListSchema)
def get_chapter_by_id(
    story_id: str, 
    chapter_id: str,
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> ChapterListSchema: 
    return story_service.get_chapter_by_id(story_id, chapter_id, user=current_user)

### Add/Remove story from favorites: POST /api/v1/stories/{story_id}/toggle-favorites ###
@router.post("/{story_id}/toggle-favorites", response_model=StoryDetailSchema)
def toogle_favorites(
    story_id: str, 
    story_service: StoryService = Depends(get_story_service),
    current_user: models.User = Depends(get_current_user)
) -> StoryDetailSchema:
    return story_service.toogle_favorites(story_id, user=current_user)