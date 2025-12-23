# AI Guide — Setup

## 🛠️ Требования для локального запуска

- Docker (рекомендуется версия 24+)
- Docker Compose (рекомендуется версия 2+; встроен в Docker Desktop на Windows/macOS)

## 🚀 1. Запуск проекта

Клонировать репозиторий:

```bash
git clone https://github.com/exxyyf/ai-adventure-guide-dth
cd ai_guide
```

## 🔑 2. Настройка ключей

Создайте файл .env в ai_guide по образцу .env.example:

```
# .env.example
MISTRAL_API_KEY=your_api_key_here
HF_TOKEN=your_api_key_here
TELEGRAM_BOT_TOKEN=your_api_key_here
RAG_PORT=8001
DATA_DIR=/app/data
API_URL=http://rag-app:8001/answer
```

##  📥 2. Скачать данные

1. Скачайте архив data/ с Google Drive:
<https://drive.google.com/file/d/1o9sy59wAFY2utvUHcCxLMOJaSIxFqkQd/view?usp=sharing>

2. Распакуйте в ai_guide проекта:

```text
ai_guide/
  data/
    chunked_texts.pkl
    embeddings.npy
    metadata.json
    wikivoyage.index
```

## ▶️ 4. Запуск сервиса


### 🐳 1. Поднять контейнеры локально
```
docker compose up -d --build
```
### 🤖 2. Зайти в телеграм бот @ai_journey_guide_bot
Набрать ```/start```, дождаться ответа от бота и задать свой вопрос. Наш бот работает на английском языке :)


### ⚠️ 3. Как отключить сервиc 
Остановить контейнеры
```docker compose down```




