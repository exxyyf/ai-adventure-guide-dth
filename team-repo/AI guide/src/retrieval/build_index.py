import pickle
import json
import numpy as np
import faiss
from datasets import load_dataset
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedder import Embedder
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")

def build_index(chunk_size=512, chunk_overlap=128):
    # Загрузка датасета
    dataset = load_dataset("bigscience-data/roots_en_wikivoyage", split="train")
    texts = dataset["text"]

    # Разбиение на чанки
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunked_texts = []
    for text in texts:
        chunked_texts.extend(splitter.split_text(text))

    # Эмбеддинги
    embedder = Embedder()
    embeddings = embedder.embed_texts(chunked_texts)

    # FAISS индекс
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Сохранение
    os.makedirs(DATA_DIR, exist_ok=True)
    faiss.write_index(index, f"{DATA_DIR}/wikivoyage.index")

    with open(f"{DATA_DIR}/chunked_texts.pkl", "wb") as f:
        pickle.dump(chunked_texts, f)

    np.save(f"{DATA_DIR}/embeddings.npy", embeddings)

    metadata = {
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "total_chunks": len(chunked_texts),
        "embedding_dim": embeddings.shape[1]
    }
    with open(f"{DATA_DIR}/metadata.json", "w") as f:
        json.dump(metadata, f)

    print("✅ FAISS index and embeddings saved to data/")
