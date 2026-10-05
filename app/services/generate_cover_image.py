import os
import asyncio
import httpx
import boto3
from app.database.database import SessionLocal
import app.database.models as models
from app.core.constants import FLUX_SCHNELL_PREDICTIONS_URL
from app.core.prompts import COVER_IMAGE_PROMPT_TEMPLATE_EN
from app.core.config import (
    REPLICATE_API_TOKEN, 
    S3_ENDPOINT_URL, 
    R2_ACCESS_KEY_ID, 
    R2_SECRET_ACCESS_KEY, 
    R2_BUCKET, 
    R2_PUBLIC_BASE_URL,
)

def build_flux_prompt(hero: str, setting: str, action: str = "exploring the area") -> str:
        style_prefix = "Whimsical children's book storybook illustration of"
        style_suffix = COVER_IMAGE_PROMPT_TEMPLATE_EN

        return f"{style_prefix} {hero}, {action} in {setting}. {style_suffix}"

async def generate_cover_image(prompt: str) -> str:
    token = REPLICATE_API_TOKEN
    if not token:
        raise RuntimeError("REPLICATE_API_TOKEN is not set")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    timeout = httpx.Timeout(30.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
        response = await client.post(
            FLUX_SCHNELL_PREDICTIONS_URL,
            json={
                "input": {
                    "prompt": prompt,
                    "aspect_ratio": "16:9",
                    "output_format": "webp",
                    "output_quality": 80,
                }
            },
        )
        response.raise_for_status()
        prediction = response.json()

        deadline = asyncio.get_running_loop().time() + 180
        while prediction["status"] not in ("succeeded", "failed", "canceled"):
            if asyncio.get_running_loop().time() > deadline:
                raise TimeoutError("Cover image generation timed out")
            await asyncio.sleep(1)
            poll = await client.get(prediction["urls"]["get"])
            poll.raise_for_status()
            prediction = poll.json()

        if prediction["status"] != "succeeded":
            raise RuntimeError(prediction.get("error") or "Cover image generation failed")

        output = prediction["output"]
        if isinstance(output, list):
            return output[0]
        return output

def _r2_client():
    return boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto",
    )

async def upload_cover(story_id: str, source_url: str) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(source_url)
        response.raise_for_status()
        body = response.content
    key = f"covers/{story_id}.webp"
    await asyncio.to_thread(
        _r2_client().put_object,
        Bucket=R2_BUCKET,
        Key=key,
        Body=body,
        ContentType="image/webp",
    )
    base = R2_PUBLIC_BASE_URL.rstrip("/")
    return f"{base}/{key}"    

async def save_cover(story_id: str, prompt: str) -> None:
    source_url = await generate_cover_image(prompt)
    image_url = await upload_cover(story_id, source_url)

    db = SessionLocal()
    try:
        story = db.query(models.Story).filter(models.Story.id == story_id).one()
        story.image_url = image_url
        db.commit()
    finally:
        db.close()        