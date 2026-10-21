import math
import os
import unittest

from app.ai.embedding.embedding_client import EmbeddingClient
from app.common.config.settings import settings
from app.llm.llm_client import LLMClient


@unittest.skipUnless(
    os.getenv("RUN_GEMINI_INTEGRATION") == "1",
    "Set RUN_GEMINI_INTEGRATION=1 to call the real Gemini API",
)
class GeminiIntegrationTest(unittest.TestCase):
    def test_embedding_api(self):
        client = EmbeddingClient(
            api_key=settings.llm_api_key,
            model=settings.embedding_model,
            dimension=settings.embedding_dimension,
        )

        vector = client.embed_query("Gemini API connectivity test")

        self.assertEqual(len(vector), settings.embedding_dimension)
        self.assertAlmostEqual(
            math.sqrt(sum(value * value for value in vector)),
            1.0,
            places=5,
        )

    def test_generation_api(self):
        client = LLMClient(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )

        answer = client.generate_answer(
            instructions="Reply with exactly GEMINI_TEST_OK.",
            prompt="Connectivity test. Reply with exactly GEMINI_TEST_OK.",
        )

        self.assertIn("GEMINI_TEST_OK", answer)


if __name__ == "__main__":
    unittest.main()
