import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
OPEN_ROUTER_TOKEN = os.getenv("OPEN_ROUTER_TOKEN")

client = OpenAI(
    api_key=OPENAI_TOKEN
)

clientOpenRouter = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPEN_ROUTER_TOKEN
)
