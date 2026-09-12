from app.schemas.story import StoryResponse
from openai import AsyncOpenAI
from app.core.config import OPENAI_API_KEY, STORY_GENERATION_PROMPT_TEMPLATE, STORY_CONTINUATION_PROMPT_TEMPLATE
from app.utils.system import get_system_prompt_from_env

class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_story(self, hero: str, setting: str, style: str) -> StoryResponse:
        system_prompt = get_system_prompt_from_env(
            params={"hero": hero, "setting": setting, "style": style}, 
            env_key=STORY_GENERATION_PROMPT_TEMPLATE
        )

        response = await self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Start the story."}
            ],
            response_format=StoryResponse,
        )

        return response.choices[0].message.parsed

    async def continue_story(self, story_id: str, chapter_id: str) -> StoryResponse:
        system_prompt = get_system_prompt_from_env(
            params={"story_id": story_id, "chapter_id": chapter_id},
            env_key=STORY_CONTINUATION_PROMPT_TEMPLATE
        )

        response = await self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
            ],
        )

        return response.choices[0].message.parsed

ai_service = AIService()