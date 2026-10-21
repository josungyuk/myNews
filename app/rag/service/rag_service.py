from app.ai.embedding.embedding_client import EmbeddingClient
from app.llm.llm_client import LLMClient
from app.rag.domain.retrieved_chunk import RetrievedChunk
from app.rag.repository.news_chunk_search_repository import NewsChunkSearchRepository


class RagService:
    def __init__(
        self,
        embedding_client: EmbeddingClient,
        search_repository: NewsChunkSearchRepository,
        llm_client: LLMClient,
        max_context_chars: int = 6000,
    ):
        self.embedding_client = embedding_client
        self.search_repository = search_repository
        self.llm_client = llm_client
        self.max_context_chars = max_context_chars

    def answer(self, question: str, limit: int = 5) -> dict:
        if not question or not question.strip():
            raise ValueError("question cannot be empty")

        query_vector = self.embedding_client.embed_query(question)
        chunks = self.search_repository.search_similar(query_vector, limit)

        if not chunks:
            return {
                "answer": "관련된 뉴스 자료를 찾지 못했습니다.",
                "sources": [],
            }

        chunks = self._select_unique_articles(chunks)
        context = self._build_context(chunks)
        instructions = (
            "You answer questions about news using only the supplied context. "
            "If the context does not contain enough information, say so. "
            "Do not invent facts or sources. Answer in Korean."
        )
        prompt = f"Question:\n{question}\n\nNews context:\n{context}"
        answer = self.llm_client.generate_answer(instructions, prompt)

        return {
            "answer": answer,
            "sources": [
                {
                    "news_id": chunk.news_id,
                    "title": chunk.title,
                    "source": chunk.source,
                    "url": chunk.url,
                }
                for chunk in chunks
            ],
        }

    def _select_unique_articles(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        selected = []
        seen_news_ids = set()

        for chunk in chunks:
            if chunk.news_id in seen_news_ids:
                continue
            selected.append(chunk)
            seen_news_ids.add(chunk.news_id)

        return selected

    def _build_context(self, chunks: list[RetrievedChunk]) -> str:
        sections = []
        total_length = 0

        for chunk in chunks:
            section = (
                f"Title: {chunk.title}\n"
                f"Source: {chunk.source}\n"
                f"Content:\n{chunk.content}"
            )
            remaining = self.max_context_chars - total_length
            if remaining <= 0:
                break

            section = section[:remaining]
            sections.append(section)
            total_length += len(section)

        return "\n\n---\n\n".join(sections)
