# import os
from app.core.prompts.prompts import PROMPTS

def get_system_prompt_from_env(env_key: str, params: dict) -> str:
    prompt = PROMPTS[env_key].format(**params)

    return prompt