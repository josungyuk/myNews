from google import genai
from google.genai import types
from google.genai import errors as genai_errors
import json
from typing import Any

class LLMClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        fallback_model: str | None = None,
        max_output_tokens: int = 512,
        client: Any | None = None,
    ):
        self.model = model
        self.fallback_model = fallback_model
        self.max_output_tokens = max_output_tokens
        self.client = client or genai.Client(api_key=api_key)

    def summarize(self, instuctions:str, prompt:str) -> str:
        response = self.client.models.generate_content(
            model = self.model,
            config = types.GenerateContentConfig(
                system_instruction=instuctions,
                temperature=0.0,
                response_mime_type="application/json",
            ),
            contents=prompt,
        )

        return json.loads(response.text)

    def generate_answer(self, instructions: str, prompt: str) -> str:
        try:
            return self._generate_answer(self.model, instructions, prompt)
        except genai_errors.APIError as error:
            can_fallback = (
                error.code in {429, 503}
                and self.fallback_model
                and self.fallback_model != self.model
            )
            if not can_fallback:
                raise

            return self._generate_answer(
                self.fallback_model,
                instructions,
                prompt,
            )

    def _generate_answer(
        self,
        model: str,
        instructions: str,
        prompt: str,
    ) -> str:
        response = self.client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=instructions,
                temperature=0.0,
                max_output_tokens=self.max_output_tokens,
            ),
            contents=prompt,
        )
        return response.text
