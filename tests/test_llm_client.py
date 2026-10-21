import unittest
from types import SimpleNamespace

from google.genai import errors as genai_errors

from app.llm.llm_client import LLMClient


class FakeModels:
    def __init__(self):
        self.models = []

    def generate_content(self, **kwargs):
        self.models.append(kwargs["model"])
        if len(self.models) == 1:
            raise genai_errors.ServerError(
                503,
                {"error": {"code": 503, "status": "UNAVAILABLE"}},
            )
        return SimpleNamespace(text="fallback answer")


class LLMClientTest(unittest.TestCase):
    def test_503_uses_fallback_model(self):
        models = FakeModels()
        client = LLMClient(
            api_key="test-key",
            model="primary-model",
            fallback_model="fallback-model",
            client=SimpleNamespace(models=models),
        )

        answer = client.generate_answer("instructions", "prompt")

        self.assertEqual(answer, "fallback answer")
        self.assertEqual(models.models, ["primary-model", "fallback-model"])


if __name__ == "__main__":
    unittest.main()
