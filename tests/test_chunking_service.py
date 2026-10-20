import hashlib
import unittest

from app.rag.service.chunking_service import ChunkingService


class ChunkingServiceTest(unittest.TestCase):
    def test_empty_content_returns_no_chunks(self):
        service = ChunkingService()

        self.assertEqual(service.chunk(news_id=1, content="   "), [])

    def test_short_content_creates_one_chunk(self):
        service = ChunkingService(chunk_size=10, overlap=2)

        chunks = service.chunk(news_id=7, content="news")

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].news_id, 7)
        self.assertEqual(chunks[0].chunk_index, 0)
        self.assertEqual(chunks[0].content, "news")

    def test_exact_chunk_size_does_not_create_overlap_only_chunk(self):
        service = ChunkingService(chunk_size=10, overlap=2)

        chunks = service.chunk(news_id=1, content="abcdefghij")

        self.assertEqual(len(chunks), 1)

    def test_long_content_preserves_overlap(self):
        service = ChunkingService(chunk_size=10, overlap=2)

        chunks = service.chunk(news_id=1, content="abcdefghijklmnop")

        self.assertEqual([chunk.content for chunk in chunks], ["abcdefghij", "ijklmnop"])
        self.assertEqual(chunks[0].content[-2:], chunks[1].content[:2])

    def test_hash_is_deterministic_hex_string(self):
        service = ChunkingService()

        chunk = service.chunk(news_id=1, content="same content")[0]

        expected_hash = hashlib.sha256(b"same content").hexdigest()
        self.assertEqual(chunk.content_hash, expected_hash)
        self.assertEqual(len(chunk.content_hash), 64)


if __name__ == "__main__":
    unittest.main()
