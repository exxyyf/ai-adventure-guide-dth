import faiss
import pickle
import numpy as np
import json
import os
from .embedder import Embedder

# Используем переменную окружения DATA_DIR, если она есть, иначе fallback на относительный путь
# DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "../../data"))
from pathlib import Path
import os

# DATA_DIR = Path(os.environ["DATA_DIR"])
# DATA_DIR = os.getenv("DATA_DIR", "/app/data")
SCRIPT_DIR = Path(__file__).resolve().parent
AI_GUIDE_DIR = SCRIPT_DIR.parents[2]
DATA_DIR = AI_GUIDE_DIR / "data"



class Retriever:
    def __init__(self):
        # Проверяем существование директории
        if not os.path.exists(DATA_DIR):
            raise FileNotFoundError(f"Data directory not found: {DATA_DIR}, {print(os.path.dirname(os.path.abspath(__file__)))}")

        # Загрузка индекса и чанков
        self.index = faiss.read_index(os.path.join(DATA_DIR, "wikivoyage.index"))
        with open(os.path.join(DATA_DIR, "chunked_texts.pkl"), "rb") as f:
            self.chunked_texts = pickle.load(f)
        self.embeddings = np.load(os.path.join(DATA_DIR, "embeddings.npy"))
        with open(os.path.join(DATA_DIR, "metadata.json"), "r") as f:
            self.metadata = json.load(f)

        self.embedder = Embedder()

    def retrieve(self, query: str, top_k=5):
        """Поиск наиболее релевантных чанков по запросу"""
        query_vec = self.embedder.embed_query(query)
        distances, indices = self.index.search(query_vec, k=top_k)
        results = [self.chunked_texts[i] for i in indices[0]]
        return results
