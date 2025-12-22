from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name="paraphrase-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        """Эмбеддинг списка текстов"""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return np.array(embeddings).astype("float32")

    def embed_query(self, query: str):
        """Эмбеддинг одного запроса"""
        vec = self.model.encode([query])
        return np.array(vec).astype("float32")
