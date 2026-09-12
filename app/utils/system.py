import os

def get_system_prompt_from_env(env_key: str, params: dict) -> str:
    raw_template = os.getenv(env_key, "")
    template = raw_template.encode('utf-8').decode('unicode_escape')

    prompt = template.format(**params)

    return prompt