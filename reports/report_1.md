## Отчет №1 по работе над командным проектом по LLM

### Сведения о проекте

**Тема проекта:** AI-гид

**Ментор:** Василий Лаврентьев

**Команда:** DreamTeamHouse

**Участники команды:**
- Лукоянова Василиса
- Лившиц Лев
- Миллер Алина
- Попов Владимир
- Михайлов Владислав

**Репозиторий проекта**

Мы ведем командную работу в двух репозиториях:

research & development – репозиторий, посвященный исследованию предметной области, доступных данных, рынка и технологий
https://github.com/exxyyf/ai-adventure-guide-dth

prod – репозиторий, содержащий код актуального решения для запуска на виртуальной машине
https://github.com/Levliv/AI-travel-guide

## Данные для проекта

Мы провели [исследование предметной области](https://github.com/exxyyf/ai-adventure-guide-dth/tree/main/research/domain) (travel-гиды), и нашли информацию по [релевантным датасетам](https://github.com/exxyyf/ai-adventure-guide-dth/tree/main/research/datasets). 

В качестве основного источника данных для реализации проекта был выбран датасет [roots_enwikivoyage](https://huggingface.co/datasets/bigscience-data/roots_en_wikivoyage). Он содержит тексты из англоязычной версии проекта Wikivoyage – бесплатный, многоязычный, открытый вики-проект Фонда Викимедиа, который создается добровольцами для написания свободных туристических путеводителей по всему миру. 

Мы планируем использовать этот датасет как базовый для RAG-системы, одной из частей нашего проекта.

Так как Wikivoyage не всегда содержит всю необходимую информацию в силу своей узкой специализации, в качестве дополнительного источника данных мы планируем использовать [API wikipedia](https://pypi.org/project/Wikipedia-API/). С помощью API можно искать релевантные статьи по ключевым словам, а также запрашивать тексты статей, их структуру и информацию о ссылках.

### Источники данных

- [roots_enwikivoyage](https://huggingface.co/datasets/bigscience-data/roots_en_wikivoyage)
- [Wikipedia](https://www.wikipedia.org/)

### Процесс получения данных

#### roots_enwikivoyage

- Скачиваем датасет с huggingface https://huggingface.co/datasets/bigscience-data/roots_en_wikivoyage в формате .parquet
- Выделяем тексты

```python
# Загрузить датасет
dataset = load_dataset("bigscience-data/roots_en_wikivoyage", split="train")

# Получить тексты
texts = dataset["text"][:10000]  # первые 10k для примера
```

#### Wikipedia API

- Устанавливаем библиотеку для работы с API https://pypi.org/project/Wikipedia-API/
- Можем найти релевантные статьи по ключевым словам или получить текст и другие атрибуты статьи из Википедии по названию
- Дополнительная информация будет использоваться, если специальный Агент определит, что RAG-система выдала неполный ответ на запрос пользователя (в силу небольшого размера базового корпуса Wikivoyage)

### Структура данных

#### roots_enwikivoyage

```
Dataset({
    features: ['meta', 'text'],
    num_rows: 24838
})
```

Пример записи из датасета:

| meta                                                                                                              | text                                                                                                                                |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| {'content_model': 'wikitext', 'language': 'en', 'title': 'The Most Beautiful Villages of France', 'type': 'text'} | The Most Beautiful Villages of France (Les Plus Beaux Villages de France) is a French association created to promote the tourist... |
#### Sample собранных данных

Более подробный сэмл данных (50 наблюдений) можно увидеть по ссылке:
https://disk.yandex.ru/d/qtaSCzNXv8T2vA

#### Объём данных

24838 статей
238513821 символов всего
min количество символов в статье 936
max количество символов в статье 14564

##### Распределение количества символов в статьях

![[char_length_dist_by_article.png]]

![[char_length_dist_by_article_lim_50000.png]]

![[char_length_dist_by_article_lim_5000.png]]

### Подготовка для RAG/LLM/агента

Датасет Wikivoyage мы подготавливаем для RAG-системы
Шаги подготовки:

1. Загрузка данных
2. Chunking (chunk_size=512, overlap=128)
3. Векторизация
4. Сохранение в векторную базу данных

Подготовку данных и бейслайн RAG-системы можно увидеть здесь:
https://github.com/exxyyf/ai-adventure-guide-dth/blob/main/baselines/RAG_AI_Guide.ipynb

Артефакты (эмбеддинги, чанки) доступны по ссылке:
https://disk.yandex.ru/d/hA0xQunkBjiiVw
