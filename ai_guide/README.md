# AI Guide — Setup


## 🚀 1. Установка окружения

Создайте conda-окружение:

```bash
conda env create -f environment.yml
conda activate ai-guide
```

## 🔑 2. Настройка ключей

Создайте файл .env в корне проекта по образцу .env.example:

```
MISTRAL_API_KEY=your_api_key_here
```

## 🔑 📥 3. Скачать данные

1. Скачайте архив data/ с Google Drive:
<https://drive.google.com/file/d/1o9sy59wAFY2utvUHcCxLMOJaSIxFqkQd/view?usp=sharing>

2. Распакуйте в корень проекта:

```text
AI-guide/
  data/
    passages.json
    embeddings.faiss
    vector_store.pkl
    ...


## ▶️ 4. Запуск RAG-пайплайна

- python main.py --q "France visa?"

- либо poetry run python main.py --q "France visa?"

Вопрос можно/нужно менять!!!

