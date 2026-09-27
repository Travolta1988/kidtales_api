from app.schemas.story import StoryResponse, ChapterGenerationSchema
from openai import AsyncOpenAI, APIError
from app.core.config import OPENAI_API_KEY
from app.core.constants import AI_MODEL, STORY_GENERATION_PROMPT_TEMPLATE, STORY_CONTINUATION_PROMPT_TEMPLATE, STORY_CONCLUSION_PROMPT_TEMPLATE
from app.utils.system import get_system_prompt_from_env
from typing import Any
import logging

logger = logging.getLogger(__name__)

class AIError(Exception):
    def __init__(self, error: APIError):
        self.message = error.message
        super().__init__(self.message)

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY, timeout=60.0)

    async def _generate(self, prompt: str, response_format: Any):
        try:
            response = await self.client.beta.chat.completions.parse(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                ],
                    response_format=response_format
            )
        except APIError as e:
            raise AIError(e) from e
            
            # 2. Собираем метрики токенов
        usage_info = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
        
        # Логируем прямо здесь (для быстрой отладки в консоли)
        print(f"📊 [Token Usage] Prompt: {usage_info['prompt_tokens']} | "
            f"Completion: {usage_info['completion_tokens']} | "
            f"Total: {usage_info['total_tokens']}")  

        return response

    # Generate story
    async def generate_story(self, hero: str, setting: str, style: str) -> StoryResponse:
        system_prompt = get_system_prompt_from_env(
            params={
                "hero": hero,
                "setting": setting, 
                "style": style
            }, 
            env_key=STORY_GENERATION_PROMPT_TEMPLATE
        )
        response = await self._generate(system_prompt, StoryResponse)
        return response.choices[0].message.parsed

    # Generate next chapter
    async def generate_next_chapter(
        self, 
        hero: str, 
        setting: str, 
        style: str, 
        chapter_number: int, 
        full_story_context: str, 
        previous_chapter_content: str,
        chapter_description: str,
        next_option: str
    ) -> ChapterGenerationSchema:

        print(f"Next option: {next_option}")
        system_prompt = get_system_prompt_from_env(
            params={
                "hero": hero, 
                "setting": setting, 
                "style": style, 
                "full_story_context": full_story_context,
                "previous_chapter_content": previous_chapter_content, 
                "chapter_number": chapter_number,
                "chapter_description": chapter_description,
                "next_option": next_option
            },
            env_key=STORY_CONTINUATION_PROMPT_TEMPLATE
        )
        response = await self._generate(system_prompt, ChapterGenerationSchema)
        return response.choices[0].message.parsed

    # Generate story end
    async def generate_story_conclusion(self, 
        hero: str, 
        setting: str, 
        style: str, 
        chapter_number: int, 
        full_story_context: str, 
        previous_chapter_content: str,
        chapter_description: str
    ) -> ChapterGenerationSchema:
        system_prompt = get_system_prompt_from_env(
            params={
                "hero": hero, 
                "setting": setting, 
                "style": style, 
                "chapter_number": chapter_number,
                "full_story_context": full_story_context,
                "previous_chapter_content": previous_chapter_content,
                "chapter_description": chapter_description
            },
            env_key=STORY_CONCLUSION_PROMPT_TEMPLATE
        )
        response = await self._generate(system_prompt, ChapterGenerationSchema)
        return response.choices[0].message.parsed

ai_service = AIService()