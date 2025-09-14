import os

import httpx
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from .config import API_CONFIG, PERSONALITY_PROMPT
from .Tools import TOOLS

load_dotenv()
OPEN_ROUTER_TOKEN = os.getenv("OPEN_ROUTER_TOKEN")


def create_agent(user: str) -> Agent:
    http_client = httpx.AsyncClient(
        headers={
            "HTTP-Referer": API_CONFIG["referer"],
            "X-Title": API_CONFIG["title"],
            "user": user,
        }
    )

    model = OpenAIChatModel(
        API_CONFIG["model"],
        provider=OpenRouterProvider(
            api_key=OPEN_ROUTER_TOKEN, http_client=http_client
        ),
        settings={
            "max_tokens": 500,
            "temperature": 1.5,
            "top_p": 0.9,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5,
        },
    )

    return Agent(model, tools=TOOLS, system_prompt=PERSONALITY_PROMPT)
