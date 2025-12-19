import faiss
import pickle
import numpy as np
import json
import os
from .embedder import Embedder

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")

class Retriever:
    def __init__(self):
        # Загрузка индекса и чанков
        self.index = faiss.read_index(f"{DATA_DIR}/wikivoyage.index")
        with open(f"{DATA_DIR}/chunked_texts.pkl", "rb") as f:
            self.chunked_texts = pickle.load(f)
        self.embeddings = np.load(f"{DATA_DIR}/embeddings.npy")
        with open(f"{DATA_DIR}/metadata.json", "r") as f:
            self.metadata = json.load(f)
        self.embedder = Embedder()

    def retrieve(self, query: str, top_k=5):
        """Поиск наиболее релевантных чанков по запросу"""
        query_vec = self.embedder.embed_query(query)
        distances, indices = self.index.search(query_vec, k=top_k)
        results = [self.chunked_texts[i] for i in indices[0]]
        return results
