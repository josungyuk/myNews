import math
import unittest
from types import SimpleNamespace

from app.ai.embedding.embedding_client import EmbeddingClient


class FakeModels:
    def __init__(self, vectors: list[list[float]]):
        self.vectors = vectors
        self.last_call = None

    def embed_content(self, **kwargs):
        self.last_call = kwargs
        return SimpleNamespace(
            embeddings=[
                SimpleNamespace(values=vector)
                for vector in self.vectors
            ]
        )


class EmbeddingClientTest(unittest.TestCase):
    def create_client(self, vectors: list[list[float]]):
        models = FakeModels(vectors)
        google_client = SimpleNamespace(models=models)
        client = EmbeddingClient(
            api_key="test-key",
            model="test-model",
            dimension=3,
            client=google_client,
        )
        return client, models

    def test_documents_use_retrieval_document_task(self):
        client, models = self.create_client([[3.0, 4.0, 0.0]])

        vectors = client.embed_documents(["news content"])

        self.assertEqual(models.last_call["model"], "test-model")
        self.assertEqual(
            models.last_call["config"].task_type,
            "RETRIEVAL_DOCUMENT",
        )
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in vectors[0])), 1.0)

    def test_query_uses_retrieval_query_task(self):
        client, models = self.create_client([[1.0, 2.0, 2.0]])

        vector = client.embed_query("interest rate news")

        self.assertEqual(
            models.last_call["config"].task_type,
            "RETRIEVAL_QUERY",
        )
        self.assertEqual(len(vector), 3)

    def test_empty_text_is_rejected(self):
        client, _ = self.create_client([[1.0, 0.0, 0.0]])

        with self.assertRaises(ValueError):
            client.embed_query("   ")

    def test_wrong_vector_dimension_is_rejected(self):
        client, _ = self.create_client([[1.0, 2.0]])

        with self.assertRaises(RuntimeError):
            client.embed_query("news")


if __name__ == "__main__":
    unittest.main()
