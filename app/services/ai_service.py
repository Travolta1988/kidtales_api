from app.schemas.story import Language
from openai import AsyncOpenAI, APIError
from app.services.streams import StoryGenerationStream, ChapterGenerationStream
from app.core.config import OPENAI_API_KEY
from app.core.constants import (
    AI_MODEL, 
    PRO_AGENT_MODEL,
    STORY_GENERATION_PROMPT_TEMPLATE,
    STORY_CONTINUATION_PROMPT_TEMPLATE,
    STORY_CONCLUSION_PROMPT_TEMPLATE,
)
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

    def stream_story(self, hero: str, setting: str, style: str, goal: str, language: Language) -> StoryGenerationStream:
        system_prompt = get_system_prompt_from_env(
            params={
                "hero": hero,
                "setting": setting, 
                "style": style,
                "goal": goal,
            }, 
            env_key=STORY_GENERATION_PROMPT_TEMPLATE[language]
        )
        return StoryGenerationStream(self.client, system_prompt, PRO_AGENT_MODEL)

    # Generate next chapter
    async def stream_chapter_next(
        self, 
        hero: str, 
        setting: str, 
        style: str, 
        goal: str,
        chapter_number: int, 
        full_story_context: str, 
        previous_chapter_content: str,
        chapter_description: str,
        next_option: str,
        language: Language
    ) -> ChapterGenerationStream:
        print(f"Next option: {next_option}")

        system_prompt = get_system_prompt_from_env(
            params={
                "hero": hero, 
                "setting": setting, 
                "style": style, 
                "goal": goal,
                "full_story_context": full_story_context,
                "previous_chapter_content": previous_chapter_content, 
                "chapter_number": chapter_number,
                "chapter_description": chapter_description,
                "next_option": next_option
            },
            env_key=STORY_CONTINUATION_PROMPT_TEMPLATE[language]
        )
        return ChapterGenerationStream(self.client, system_prompt, AI_MODEL)

    # Generate story end
    async def stream_chapter_conclusion(self, 
        hero: str, 
        setting: str, 
        style: str, 
        goal: str,
        chapter_number: int, 
        full_story_context: str, 
        previous_chapter_content: str,
        chapter_description: str,
        language: Language
    ) -> ChapterGenerationStream:
        system_prompt = get_system_prompt_from_env(
            params={
                "hero": hero, 
                "setting": setting, 
                "style": style,
                "goal": goal,
                "chapter_number": chapter_number,
                "full_story_context": full_story_context,
                "previous_chapter_content": previous_chapter_content,
                "chapter_description": chapter_description
            },
            env_key=STORY_CONCLUSION_PROMPT_TEMPLATE[language]
        )
        return ChapterGenerationStream(self.client, system_prompt)

ai_service = AIService()
