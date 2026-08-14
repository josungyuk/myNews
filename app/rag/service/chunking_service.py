import hashlib

from app.rag.domain.news_chunk import NewsChunk

class ChunkingService:
    def __init__(self, chunk_size: int = 1500, overlap:int = 200):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, news_id: int, content: str) -> list[NewsChunk]:
        if not content or not content.strip():
            return []

        chunks: list[NewsChunk] = []
        start = 0

        while start < len(content):
            end = min(start + self.chunk_size, len(content))
            chunk_content = content[start:end].strip()

            content_hash = hashlib.sha256(chunk_content.encode("utf-8")).hexdigest()

            chunks.append(
                NewsChunk(
                    news_id=news_id,
                    chunk_index=len(chunks),
                    content=chunk_content,
                    content_hash=content_hash,
                )
            )

            if end == len(content):
                break

            start = end - self.overlap

        return chunks