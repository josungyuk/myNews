import math
from typing import Any

from google import genai
from google.genai import types


class EmbeddingClient:
    def __init__(
        self,
        api_key: str,
        model: str,
        dimension: int,
        client: Any | None = None,
    ):
        if dimension <= 0:
            raise ValueError("dimension must be greater than 0")

        self.model = model
        self.dimension = dimension
        self.client = client or genai.Client(api_key=api_key)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self._validate_texts(texts)
        return self._embed(texts, task_type="RETRIEVAL_DOCUMENT")

    def embed_query(self, text: str) -> list[float]:
        self._validate_texts([text])
        return self._embed([text], task_type="RETRIEVAL_QUERY")[0]

    def _embed(
        self,
        texts: list[str],
        task_type: str,
    ) -> list[list[float]]:
        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=self.dimension,
            ),
        )

        if not response.embeddings:
            raise RuntimeError("The embedding API returned no embeddings")

        vectors = [
            self._normalize(list(embedding.values or []))
            for embedding in response.embeddings
        ]

        if len(vectors) != len(texts):
            raise RuntimeError(
                "The embedding API returned an unexpected number of embeddings"
            )

        return vectors

    def _normalize(self, vector: list[float]) -> list[float]:
        if len(vector) != self.dimension:
            raise RuntimeError(
                f"Expected embedding dimension {self.dimension}, "
                f"but received {len(vector)}"
            )

        magnitude = math.sqrt(sum(value * value for value in vector))

        if magnitude == 0:
            raise RuntimeError("The embedding API returned a zero vector")

        return [value / magnitude for value in vector]

    def _validate_texts(self, texts: list[str]) -> None:
        if not texts:
            raise ValueError("At least one text is required")

        if any(not text or not text.strip() for text in texts):
            raise ValueError("Embedding text cannot be empty")
