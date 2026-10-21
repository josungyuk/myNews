import unittest

from fastapi.testclient import TestClient
from google.genai import errors as genai_errors

from app.main import app
from app.rag.controller import rag_controller


class UnavailableEmbeddingClient:
    def embed_query(self, text: str):
        raise genai_errors.ServerError(
            503,
            {
                "error": {
                    "code": 503,
                    "message": "high demand",
                    "status": "UNAVAILABLE",
                }
            },
        )


class GeminiErrorHandlerTest(unittest.TestCase):
    def test_gemini_unavailable_returns_http_503(self):
        app.dependency_overrides[rag_controller.get_embedding_client] = (
            lambda: UnavailableEmbeddingClient()
        )

        try:
            response = TestClient(app).post(
                "/rag/ask",
                json={"question": "test question"},
            )
        finally:
            app.dependency_overrides.clear()

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.headers["retry-after"], "30")
        self.assertEqual(
            response.json(),
            {"detail": "Gemini is temporarily unavailable. Please try again later."},
        )


if __name__ == "__main__":
    unittest.main()
