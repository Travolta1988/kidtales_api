import os
from time import sleep
from app.schemas.story import ChapterResponse, StoryOption
from openai import AsyncOpenAI
from app.core.config import OPENAI_API_KEY

# class AIService:
#     def __init__(self):
#         self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
#
#     async def generate_first_chapter(self, hero_name: str, setting: str, style: str) -> ChapterResponse:
#         system_prompt = (
#             f"Ты — профессиональный сказочник. Пиши в стиле '{style}'. "
#             f"Создай первую главу сказки про героя по имени {hero_name} в локации '{setting}'. "
#             "В конце главы обязательно предложи ровно 3 варианта дальнейших действий."
#         )
#
#         # Используем Structured Outputs (или response_format) для получения строгого JSON
#         response = await self.client.beta.chat.completions.parse(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": "Начни сказку."}
#             ],
#             response_format=ChapterResponse, # Pydantic схема гарантирует валидный ответ!
#         )
#
#         # Возвращаем уже распарсенный Pydantic-объект
#         return response.choices[0].message.parsed
#
# # Создаем синглтон сервиса
# ai_service = AIService()

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_first_chapter(self, hero_name: str, setting: str, style: str) -> ChapterResponse:
        system_prompt = (
            f"Ты — профессиональный сказочник. Пиши в стиле '{style}'. "
            f"Создай первую главу сказки про героя по имени {hero_name} в локации '{setting}'. "
            "В конце главы обязательно предложи ровно 3 варианта дальнейших действий."
        )

        sleep(1)

        return ChapterResponse(
        story_id="test_id_12121",
        chapter_number=2,
        title=f"adadadad",
        content=f"В локации  началась сказка в стиле asdadsadasdasd asdasdadadasd...",
        options=[
            StoryOption(option_id=1, text="Пойти налево в темный лес"),
            StoryOption(option_id=2, text="Пойти направо к старой заброшенной мельнице"),
            StoryOption(option_id=3, text="Остаться на месте и зажечь костер")
        ]
    )

ai_service = AIService()