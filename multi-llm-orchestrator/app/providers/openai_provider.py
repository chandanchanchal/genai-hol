import os
from openai import OpenAI
from app.providers.base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, messages: list, model: str) -> dict:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )

        return {
            "text": response.choices[0].message.content,
            "usage": response.usage
        }
