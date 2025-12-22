import json
from typing import Optional, Dict
from dotenv import load_dotenv
from mistralai import Mistral  
import os

# load_dotenv()

if not os.getenv("MISTRAL_API_KEY"):
    load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

class QuestionUnderstanding:
    def __init__(self, model_name: str = "mistral-small-latest"):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model_name = model_name

    def analyze(self, query: str) -> Dict:
        """Проводит LLM-анализ пользовательского запроса и возвращает структуру."""

        system_prompt = """
You are a travel-domain assistant specializing in understanding short queries. 
Your task is to extract structure from ambiguous user messages.

Return ONLY valid JSON. No explanations.

JSON schema:
{
  "intent": "one of: information, recommendation, navigation, visa, safety, transport, accommodation, unknown",
  "entities": ["list of locations found (cities, countries, landmarks)"],
  "clarified_query": "a rewritten, clearer version of the question",
  "needs_more_info": true/false
}

Rules:
- “intent” should reflect what the user wants.
- If the query is very short, incomplete, or missing details → needs_more_info = true.
- If no location found → entities = [].
- clarified_query must be optimized for retrieval.
"""

        user_prompt = f"User query: {query}\nReturn JSON:"

        response = self.client.chat.complete(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )

        data = response.choices[0].message.content

        # Обработка ошибок: иногда модель может добавить текст до/после JSON
        json_str = self._extract_json(data)
        return json.loads(json_str)

    @staticmethod
    def _extract_json(text: str) -> str:
        """Извлекает JSON из текста (на случай, если модель добавит лишнее)."""
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("No JSON found in LLM output")
        return text[start : end + 1]


import sys

if __name__ == "__main__":
    # Проверяем, что аргумент передан
    if len(sys.argv) < 2:
        print("Usage: python question_understanding.py \"your question here\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    q = QuestionUnderstanding()

    try:
        result = q.analyze(query)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

