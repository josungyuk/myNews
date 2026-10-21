import unittest

from app.rag.domain.news_chunk import NewsChunk
from app.rag.service.chunk_embedding_service import ChunkEmbeddingService


class FakeEmbeddingClient:
    def __init__(self):
        self.texts = None

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.texts = texts
        return [[1.0, 0.0], [0.0, 1.0]]


class ChunkEmbeddingServiceTest(unittest.TestCase):
    def test_embed_attaches_vectors_to_chunks(self):
        client = FakeEmbeddingClient()
        service = ChunkEmbeddingService(client)
        chunks = [
            NewsChunk(1, 0, "first", "hash-1"),
            NewsChunk(1, 1, "second", "hash-2"),
        ]

        embedded = service.embed(chunks)

        self.assertEqual(client.texts, ["first", "second"])
        self.assertEqual(embedded[0].embedding, [1.0, 0.0])
        self.assertEqual(embedded[1].embedding, [0.0, 1.0])
        self.assertIsNone(chunks[0].embedding)

    def test_empty_chunks_do_not_call_embedding_client(self):
        client = FakeEmbeddingClient()
        service = ChunkEmbeddingService(client)

        self.assertEqual(service.embed([]), [])
        self.assertIsNone(client.texts)


if __name__ == "__main__":
    unittest.main()
