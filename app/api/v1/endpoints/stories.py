from fastapi import APIRouter, HTTPException
from app.schemas.story import ChapterResponse, StoryOption, StoryCreateRequest
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/", response_model=ChapterResponse)
async def create_story(payload: StoryCreateRequest):
    # call to ai_generator
    try:
        chapter = await ai_service.generate_first_chapter(
            hero_name=payload.hero_name,
            setting=payload.setting,
            style=payload.style
        )
        return chapter
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации сказки: {str(e)}")
    # save result to database
    return ChapterResponse(
        story_id="test_story_1",
        chapter_number=1,
        title=f"Приключение героя {payload.hero_name}",
        content=f"В локации '{payload.setting}' началась сказка в стиле {payload.style}...",
        options=[
            StoryOption(option_id=1, text="Пойти налево в темный лес"),
            StoryOption(option_id=2, text="Пойти направо к старой заброшенной мельнице"),
            StoryOption(option_id=3, text="Остаться на месте и зажечь костер")
        ]
    )

@router.post("/{story_id}/continue", response_model=ChapterResponse)
async def continue_chapter(payload: StoryOption, story_id: str):
    return ChapterResponse(
        story_id=story_id,
        chapter_number=2,
        title=f"adadadad",
        content=f"В локации  началась сказка в стиле asdadsadasdasd asdasdadadasd...",
        options=[]
    )

# from fastapi import APIRouter, HTTPException
# from app.schemas.story import ChapterResponse, StoryOption, StoryCreateRequest
# from app.services.ai_service import ai_service
#
# router = APIRouter()
#
# @router.post("/", response_model=ChapterResponse)
# async def create_story(payload: StoryCreateRequest):
#     try:
#         chapter = await ai_service.generate_first_chapter(
#             hero_name=payload.hero_name,
#             setting=payload.setting,
#             style=payload.style
#         )
#         return chapter
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Ошибка генерации сказки: {str(e)}")