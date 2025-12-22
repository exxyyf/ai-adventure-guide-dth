# FROM python:3.11-slim

# # Системные зависимости
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     git \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# COPY . .

# ENV PYTHONPATH=/app
# ENV DATA_DIR=/app/data

# EXPOSE 8001

# CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8001"]

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8001"]
