import unittest

from app.rag.domain.retrieved_chunk import RetrievedChunk
from app.rag.service.rag_service import RagService


class FakeEmbeddingClient:
    def embed_query(self, text: str) -> list[float]:
        return [1.0, 0.0]


class FakeSearchRepository:
    def __init__(self, chunks: list[RetrievedChunk]):
        self.chunks = chunks
        self.last_query = None
        self.last_limit = None

    def search_similar(self, query_vector: list[float], limit: int):
        self.last_query = query_vector
        self.last_limit = limit
        return self.chunks


class FakeLLMClient:
    def __init__(self):
        self.prompt = None

    def generate_answer(self, instructions: str, prompt: str) -> str:
        self.prompt = prompt
        return "테스트 답변"


class RagServiceTest(unittest.TestCase):
    def test_answer_retrieves_context_and_sources(self):
        chunks = [
            RetrievedChunk(
                news_id=1,
                chunk_index=0,
                content="금리가 동결되었습니다.",
                title="금리 뉴스",
                source="YTN",
                url="https://example.com/news/1",
            )
        ]
        search = FakeSearchRepository(chunks)
        llm = FakeLLMClient()
        service = RagService(FakeEmbeddingClient(), search, llm)

        result = service.answer("금리 뉴스가 뭐야?", limit=3)

        self.assertEqual(result["answer"], "테스트 답변")
        self.assertEqual(result["sources"][0]["news_id"], 1)
        self.assertEqual(search.last_query, [1.0, 0.0])
        self.assertEqual(search.last_limit, 3)
        self.assertIn("금리가 동결되었습니다.", llm.prompt)

    def test_answer_returns_empty_sources_when_no_chunk_matches(self):
        search = FakeSearchRepository([])
        llm = FakeLLMClient()
        service = RagService(FakeEmbeddingClient(), search, llm)

        result = service.answer("없는 뉴스")

        self.assertEqual(result["sources"], [])
        self.assertIn("찾지 못했습니다", result["answer"])
        self.assertIsNone(llm.prompt)


if __name__ == "__main__":
    unittest.main()
