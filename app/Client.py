import os

from dotenv import load_dotenv
import httpx
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from .Tools import TOOLS
from .config import PERSONALITY_PROMPT

load_dotenv()
OPEN_ROUTER_TOKEN = os.getenv("OPEN_ROUTER_TOKEN")

http_client = httpx.AsyncClient(
    headers={
        "HTTP-Referer": "lunita.me",
        "X-Title": "Lunita",
        "user": "user_1",
    }
)

model = OpenAIChatModel(
    "@preset/lunita",
    provider=OpenRouterProvider(api_key=OPEN_ROUTER_TOKEN, http_client=http_client),
    settings={
        "max_tokens": 500,
        "temperature": 1.5,
        "top_p": 0.9,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5,
    },
)

agent = Agent(model, tools=TOOLS, system_prompt=PERSONALITY_PROMPT)
