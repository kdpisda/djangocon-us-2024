import json
import logging

from django.conf import settings
from openai import OpenAI

from cms.models.gpt import GPTLog


class ChatGPTClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.logger = logging.getLogger(__name__)

    def log_prompt(self, prompt, model, response):
        try:
            GPTLog.objects.create(
                model=model,
                prompt=prompt,
                response=response,
            )
            self.logger.info("Logged GPT prompt")
        except Exception as err:
            self.logger.error(f"Error logging GPT prompt: {err}")

    def run_prompt(self, prompt, model="gpt-4o"):
        res = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        response = res.choices[0].message.content
        self.log_prompt(prompt, model, response)
        return response

    def get_song_summary(self, lyrics):
        prompt = (
            f"Please provide a one-line summary of the song "
            f"with the following lyrics:\n{lyrics}"  # noqa
        )
        return self.run_prompt(prompt)

    def get_countries(self, lyrics):
        prompt = (
            f"Extract the names of countries mentioned in the "
            f"following song lyrics.\nReturn the result strictly "
            f"in a list format like this: `['India', 'USA']`.\n\n"
            "Ignore names of continents, States and cities, "
            "only focus on countries. Also, I don't want any formatting"
            "such as ```python or ```json or anything similar. "
            "I just want plain list format as shared above.\n"
            f"Lyrics:\n{lyrics}"  # noqa
        )
        res = self.run_prompt(prompt)
        res = res.replace("```", "")
        res = res.replace("'", '"')
        return json.loads(res)
