# import os
from app.core.prompts import PROMPTS

def get_system_prompt_from_env(env_key: str, params: dict) -> str:
    prompt = PROMPTS[env_key].format(**params)
    # raw_template = os.getenv(env_key, "")
    # template = raw_template.encode('utf-8').decode('unicode_escape')

    # prompt = template.format(**params)
    return prompt