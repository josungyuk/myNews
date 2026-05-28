from google import genai
from google.genai import types
import json

class LLMClient:
    def __init__(self, api_key: str, model: str):
        self.model = model
        self.client = genai.Client(api_key=api_key)

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