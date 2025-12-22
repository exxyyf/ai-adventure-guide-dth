FROM python:3.10-slim

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# рабочая директория
WORKDIR /app

COPY requirements.txt /app/requirements.txt

# устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . .

# Объявляем volume для данных RAG (индекс, чанки текстов, эмбеддинги и мета данные)
VOLUME ["/app/data"]


CMD ["bash"] 
# Для запуска — через docker run … python -m src.main