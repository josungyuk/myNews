from dataclasses import replace

from app.ai.embedding.embedding_client import EmbeddingClient
from app.rag.domain.news_chunk import NewsChunk


class ChunkEmbeddingService:
    def __init__(self, embedding_client: EmbeddingClient):
        self.embedding_client = embedding_client

    def embed(self, chunks: list[NewsChunk]) -> list[NewsChunk]:
        if not chunks:
            return []

        vectors = self.embedding_client.embed_documents(
            [chunk.content for chunk in chunks]
        )

        return [
            replace(chunk, embedding=vector)
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
