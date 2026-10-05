from openai import AsyncOpenAI, APIError
from app.schemas.ai import AIGeneratedStoryResponse, AIGeneratedChapterResponse
from collections.abc import AsyncIterator
from app.core.constants import (
    AI_MODEL
)

class AIError(Exception):
    def __init__(self, error: APIError):
        self.message = error.message
        super().__init__(self.message)

class StoryGenerationStream:
    """Async iterator of model text deltas. After iteration, `parsed` holds the full object."""

    def __init__(self, client: AsyncOpenAI, prompt: str, model: str):
        self._client = client
        self._prompt = prompt
        self._model = model
        self.parsed: AIGeneratedStoryResponse | None = None

    async def __aiter__(self) -> AsyncIterator[str]:
        try:
            async with self._client.chat.completions.stream(
                model=self._model,
                messages=[
                    {"role": "system", "content": self._prompt},
                ],
                response_format=AIGeneratedStoryResponse,
                stream_options={"include_usage": True},
            ) as stream:
                async for event in stream:
                    if event.type == "content.delta" and event.delta:
                        yield event.delta
                final = await stream.get_final_completion()
        except APIError as e:
            raise AIError(e) from e

        self.parsed = final.choices[0].message.parsed
        if final.usage:
            print(
                f"📊 [Token Usage] Prompt: {final.usage.prompt_tokens} | "
                f"Completion: {final.usage.completion_tokens} | "
                f"Total: {final.usage.total_tokens}"
            )

class ChapterGenerationStream:
    """Async iterator of model text deltas. After iteration, `parsed` holds the full object."""

    def __init__(self, client: AsyncOpenAI, prompt: str, model: str = AI_MODEL):
        self._client = client
        self._prompt = prompt
        self._model = model
        self.parsed: AIGeneratedChapterResponse | None = None

    async def __aiter__(self) -> AsyncIterator[str]:
        try:
            async with self._client.chat.completions.stream(
                model=self._model,
                messages=[
                    {"role": "system", "content": self._prompt},
                ],
                response_format=AIGeneratedChapterResponse,
                stream_options={"include_usage": True},
            ) as stream:
                async for event in stream:
                    if event.type == "content.delta" and event.delta:
                        yield event.delta
                final = await stream.get_final_completion()
        except APIError as e:
            raise AIError(e) from e

        self.parsed = final.choices[0].message.parsed
        if final.usage:
            print(
                f"📊 [Token Usage] Prompt: {final.usage.prompt_tokens} | "
                f"Completion: {final.usage.completion_tokens} | "
                f"Total: {final.usage.total_tokens}"
            )

