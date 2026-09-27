import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")